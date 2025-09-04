import pycountry
import models
import factories
import factory
import random
from sqlalchemy.exc import IntegrityError
from sqlalchemy import not_

from factory.alchemy import SQLAlchemyModelFactory
from tqdm import tqdm
from config import DATA_GENERATION_SIZE
from database import engine, Base, SessionLocal


def seed_regions(session):
    """Seeds the regions table from pycountry."""
    session.query(models.Region).delete()
    regions_to_add = [
        models.Region(id=country.alpha_3, name=country.name)
        for country in pycountry.countries
    ]
    session.add_all(regions_to_add)
    session.commit()


def safe_create_batch(factory_class, num, session):
    """Safely create batch of records handling potential duplicates."""
    created = 0
    attempts = 0
    max_attempts = num * 3

    pbar = tqdm(total=num, desc=f"Creating {factory_class._meta.model.__name__}")
    while created < num and attempts < max_attempts:
        try:
            factory_class()
            session.flush()
            created += 1
            pbar.update(1)
        except IntegrityError:
            session.rollback()
            attempts += 1
            continue
        except Exception:
            session.rollback()
            raise

    pbar.close()
    if created < num:
        print(
            f"Warning: Could only create {created}/{num} unique {factory_class._meta.model.__name__} instances."
        )
    return created


def run_seeder():
    """Seeds the database with structured, interconnected data."""
    print("Initializing database...")
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    session = SessionLocal()

    try:
        for factory_class in SQLAlchemyModelFactory.__subclasses__():
            factory_class._meta.sqlalchemy_session = session
        if hasattr(factories, "fake"):
            factories.fake.unique.clear()

        size = DATA_GENERATION_SIZE

        print("Seeding regions...")
        seed_regions(session)

        print("\nSeeding independent lookup tables...")
        independent_tasks = [
            ("Business Categories", factories.BusinessCategoryFactory, int(size * 0.2)),
            ("Business Phases", factories.BusinessPhaseFactory, 4),
            ("Business Roles", factories.BusinessRoleFactory, 4),
            ("Business Skills", factories.BusinessSkillFactory, 15),
            ("Business Types", factories.BusinessTypeFactory, 4),
            ("Connection Types", factories.ConnectionTypeFactory, 4),
            ("Industry Categories", factories.IndustryCategoryFactory, int(size * 0.2)),
            ("Mastermind Roles", factories.MastermindRoleFactory, 4),
            ("Strength Categories", factories.StrengthCategoryFactory, 4),
            ("Subscriptions", factories.SubscriptionFactory, 3),
            ("Daily Activities", factories.DailyActivityFactory, int(size * 0.2)),
            ("Skills", factories.SkillFactory, 50),
            # NEW: Create industries which will be linked to categories by the factory.
            ("Industries", factories.IndustryFactory, int(size * 0.4)),
        ]

        for description, factory_class, num in tqdm(
            independent_tasks, desc="Independent Tables"
        ):
            factory_class.create_batch(num)
        session.commit()
        print("Independent tables seeded.")

        print(f"\nCreating {size} core User objects...")
        users = factories.UserFactory.create_batch(size)
        session.commit()
        print("Users created and committed.")

        print("\nBuilding 1-to-1 objects for each user (Businesses, Logins, etc)...")
        objects_to_add = []
        for user in tqdm(users, desc="Creating User-specific entities"):
            objects_to_add.append(factories.BusinessFactory.build(operator=user))
            objects_to_add.append(factories.UserLoginFactory.build(user=user))
            objects_to_add.append(factories.IdeaFactory.build(submitter=user))
            objects_to_add.append(factories.UserPostFactory.build(poster=user))
            objects_to_add.append(factories.UserSubscriptionFactory.build(user=user))

        print(f"Bulk saving {len(objects_to_add)} user-dependent objects...")
        session.add_all(objects_to_add)
        session.commit()
        print("User-dependent objects saved.")

        print("\nCreating secondary core objects like Projects...")
        num_projects = int(size * 0.4)
        project_managers = random.sample(users, min(len(users), num_projects))
        projects = []
        if project_managers:
            projects = factories.ProjectFactory.create_batch(
                len(project_managers), manager=factory.Iterator(project_managers)
            )
            session.commit()
        print(f"{len(projects)} projects created.")

        print("\nBuilding logical and random relationships...")

        print("Creating logical business connections...")
        all_businesses = session.query(models.Business).all()
        connections_to_add = []
        connection_type = (
            session.query(models.ConnectionType)
            .filter(not_(models.ConnectionType.name.in_(["Investor", "Customer"])))
            .first()
        )

        for business in tqdm(all_businesses, desc="Finding Partners"):
            partner = factories.get_complementary_business(session, business)
            if partner and connection_type:
                connections_to_add.append(
                    factories.BusinessConnectionFactory.build(
                        initiating_business=business,
                        receiving_business=partner,
                        connection_type=connection_type,
                    )
                )
        session.add_all(connections_to_add)
        session.commit()
        print(f"Created {len(connections_to_add)} logical business connections.")

        many_to_many_tasks = [
            ("Idea Votes", factories.IdeaVoteFactory, size * 2),
            ("User Skills", factories.UserSkillFactory, size),
            ("User Strengths", factories.UserStrengthFactory, size),
            (
                "Daily Activity Enrolments",
                factories.DailyActivityEnrolmentFactory,
                size,
            ),
            (
                "Project Business Categories",
                factories.ProjectBusinessCategoryFactory,
                int(size * 0.6),
            ),
            (
                "Project Business Skills",
                factories.ProjectBusinessSkillFactory,
                int(size * 0.6),
            ),
            ("Project Regions", factories.ProjectRegionFactory, int(size * 0.6)),
            # NEW: Create BusinessStrengths which will be linked to BusinessRoles by the factory.
            ("Business Strengths", factories.BusinessStrengthFactory, size),
            # NEW: Create the links between connections and mastermind roles.
            (
                "Connection Mastermind Roles",
                factories.ConnectionMastermindRoleFactory,
                int(size * 0.5),
            ),
        ]

        for description, factory_class, num in many_to_many_tasks:
            if num > 0:
                safe_create_batch(factory_class, num, session)
                session.commit()

        print("Secondary objects and relationships saved.")
        print("\nData generation complete!")

    except Exception as e:
        print(f"\nAn error occurred: {e}")
        import traceback

        traceback.print_exc()
        session.rollback()
    finally:
        session.close()
