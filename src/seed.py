import pycountry
import models
import factories

from factory.alchemy import SQLAlchemyModelFactory
from tqdm import tqdm
from config import DATA_GENERATION_SIZE
from database import engine, Base, SessionLocal


def seed_regions(session):
    session.query(models.Region).delete()

    regions_to_add = [
        models.Region(id=country.alpha_3, name=country.name)
        for country in pycountry.countries
    ]

    session.add_all(regions_to_add)

def run_seeder():
    print("Initializing database...")

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    session = SessionLocal()

    try:
        for factory_class in SQLAlchemyModelFactory.__subclasses__():
            factory_class._meta.sqlalchemy_session = session
        if hasattr(factories, 'fake'):
            factories.fake.unique.clear()

        print("Seeding regions...")

        seed_regions(session)
        session.commit()

        size = DATA_GENERATION_SIZE

        print(f"Building entity objects with base size: {size}...\n")

        level_0_tasks = [
            ("Users", factories.UserFactory, size),
            ("Business Categories", factories.BusinessCategoryFactory, int(size * 0.2)),
            ("Business Phases", factories.BusinessPhaseFactory, 4),
            ("Business Roles", factories.BusinessRoleFactory, 4),
            ("Business Skills", factories.BusinessSkillFactory, 4),
            ("Business Types", factories.BusinessTypeFactory, 4),
            ("Connection Types", factories.ConnectionTypeFactory, 4),
            ("Daily Activities", factories.DailyActivityFactory, int(size * 0.2)),
            ("Industry Categories", factories.IndustryCategoryFactory, int(size * 0.2)),
            ("Mastermind Roles", factories.MastermindRoleFactory, 4),
            ("Strength Categories", factories.StrengthCategoryFactory, 4),
            ("Subscriptions", factories.SubscriptionFactory, 3),
        ]

        level_1_tasks = [
            ("Businesses", factories.BusinessFactory, int(size * 0.6)),
            ("Business Strengths", factories.BusinessStrengthFactory, int(size * 0.4)),
            ("Case Studies", factories.CaseStudyFactory, int(size * 0.4)),
            ("Ideas", factories.IdeaFactory, size),
            ("Industries", factories.IndustryFactory, int(size * 0.4)),
            ("Skill Categories", factories.SkillCategoryFactory, int(size * 0.2)),
            ("Strengths", factories.StrengthFactory, int(size * 0.4)),
            ("User Logins", factories.UserLoginFactory, size),
            ("Projects", factories.ProjectFactory, int(size * 0.4)),
            ("User Posts", factories.UserPostFactory, size),
        ]

        level_2_tasks = [
            ("Business Connections", factories.BusinessConnectionFactory, int(size * 0.8)),
            ("Daily Activity Enrolments", factories.DailyActivityEnrolmentFactory, size),
            ("Idea Votes", factories.IdeaVoteFactory, size * 2),
            ("Notifications", factories.NotificationFactory, size * 2),
            ("Skills", factories.SkillFactory, int(size * 0.6)),
            ("User Business Strengths", factories.UserBusinessStrengthFactory, size),
            ("User Daily Activity Progress", factories.UserDailyActivityProgressFactory, size * 2),
            ("User Strengths", factories.UserStrengthFactory, size),
            ("User Subscriptions", factories.UserSubscriptionFactory, int(size * 0.8)),
            ("Project Business Categories", factories.ProjectBusinessCategoryFactory, int(size * 0.6)),
            ("Project Business Skills", factories.ProjectBusinessSkillFactory, int(size * 0.6)),
            ("Project Regions", factories.ProjectRegionFactory, int(size * 0.6)),
        ]

        level_3_tasks = [
            ("Connection Mastermind Roles", factories.ConnectionMastermindRoleFactory, int(size * 0.4)),
            ("User Skills", factories.UserSkillFactory, size),
        ]

        all_levels = [
            ("Level 0", level_0_tasks),
            ("Level 1", level_1_tasks),
            ("Level 2", level_2_tasks),
            ("Level 3", level_3_tasks),
        ]

        for level_name, tasks in all_levels:
            print(f"--- Preparing {level_name} Objects ---")
            all_objects_for_level = []

            for description, factory_class, num_to_create in tqdm(tasks, desc="Building objects"):
                built_objects = factory_class.build_batch(num_to_create)
                all_objects_for_level.extend(built_objects)

            print(f"Bulk saving {len(all_objects_for_level)} objects for {level_name}...")

            session.add_all(all_objects_for_level)
            session.commit()

            print(f"{level_name} complete.\n")
        print("Data generation complete!")

    except Exception as e:
        print(f"\nAn error occurred: {e}")
        session.rollback()
    finally:
        session.close()
