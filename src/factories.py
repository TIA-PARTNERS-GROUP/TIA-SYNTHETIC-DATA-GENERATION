import os
import random
import factory
import models

from datetime import timedelta
from factory.alchemy import SQLAlchemyModelFactory
from faker import Faker
from sqlalchemy import func


fake = Faker()

class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.User

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    contact_email = factory.LazyAttribute(lambda o: f"{o.first_name}.{o.last_name}@example.com".lower())
    contact_phone_no = factory.LazyAttribute(lambda _: fake.msisdn()[:10])

class BusinessCategoryFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.BusinessCategory

    name = factory.Faker('company')

class BusinessPhaseFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.BusinessPhase

    name = factory.Iterator(['Startup', 'Growth', 'Mature', 'Decline'])

class BusinessRoleFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.BusinessRole

    name = factory.Iterator(['Founder', 'Investor', 'Advisor', 'Employee'])

class BusinessSkillFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.BusinessSkill

    id = factory.Sequence(lambda n: n + 1)
    name = factory.Iterator(['Marketing', 'Sales', 'Finance', 'Operations'])

class BusinessTypeFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.BusinessType

    name = factory.Iterator(['SaaS', 'E-commerce', 'Consulting', 'Manufacturing'])

class ConnectionTypeFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.ConnectionType

    name = factory.Iterator(['Partnership', 'Supplier', 'Customer', 'Investor'])

class DailyActivityFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.DailyActivity

    name = factory.Faker('word')
    description = factory.Faker('sentence')

class IndustryCategoryFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.IndustryCategory

    name = factory.Faker('job')

class MastermindRoleFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.MastermindRole

    name = factory.Iterator(['Leader', 'Strategist', 'Implementer', 'Innovator'])

class StrengthCategoryFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.StrengthCategory

    name = factory.Iterator(['Technical', 'Business', 'Creative', 'Leadership'])

class SubscriptionFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.Subscription

    name = factory.Iterator(['Basic', 'Pro', 'Enterprise'])
    price = factory.LazyAttribute(lambda _: round(random.uniform(10, 500), 2))
    valid_days = factory.LazyAttribute(lambda _: random.randint(30, 365))
    valid_months = factory.LazyAttribute(lambda _: random.randint(1, 12))

class BusinessFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.Business

    name = factory.Faker('company')
    operator = factory.SubFactory(UserFactory)
    business_type = factory.SubFactory(BusinessTypeFactory)
    business_category = factory.SubFactory(BusinessCategoryFactory)
    phase = factory.SubFactory(BusinessPhaseFactory)
    tagline = factory.Faker('catch_phrase')
    website = factory.Faker('url')
    description = factory.Faker('paragraph')
    address = factory.Faker('street_address')
    city = factory.Faker('city')

class BusinessStrengthFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.BusinessStrength

    name = factory.Faker('job')
    role = factory.SubFactory(BusinessRoleFactory)
    phase = factory.SubFactory(BusinessPhaseFactory)

class CaseStudyFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.CaseStudy

    title = factory.Faker('sentence')
    content = factory.Faker('text')
    thumbnail = factory.LazyAttribute(lambda _: f"https://example.com/images/{fake.uuid4()}.jpg")
    video_url = factory.LazyAttribute(lambda _: f"https://example.com/videos/{fake.uuid4()}")
    published = True
    owner = factory.SubFactory(UserFactory)

class IdeaFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.Idea

    id = factory.Sequence(lambda n: n + 1)
    content = factory.Faker('paragraph')
    submitter = factory.SubFactory(UserFactory)

class IndustryFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.Industry

    name = factory.Faker('job')
    picture = factory.LazyAttribute(lambda _: f"https://example.com/images/{fake.uuid4()}.jpg")
    category = factory.SubFactory(IndustryCategoryFactory)

class SkillCategoryFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.SkillCategory

    name = factory.Faker('job')
    business_type = factory.SubFactory(BusinessTypeFactory)

class StrengthFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.Strength

    name = factory.Faker('job')
    category = factory.SubFactory(StrengthCategoryFactory)

class UserLoginFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.UserLogin

    user = factory.SubFactory(UserFactory)
    login_email = factory.LazyAttribute(lambda o: o.user.contact_email)
    password_hash = factory.LazyAttribute(lambda _: os.urandom(70))
    password_reset_token = None
    password_reset_requested_timestamp = None

class BusinessConnectionFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.BusinessConnection

    initiating_business = factory.SubFactory(BusinessFactory)
    receiving_business = factory.SubFactory(BusinessFactory)
    connection_type = factory.SubFactory(ConnectionTypeFactory)
    active = True
    date_initiated = factory.Faker('date_time_this_year')

class DailyActivityEnrolmentFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.DailyActivityEnrolment

    activity = factory.SubFactory(DailyActivityFactory)
    user = factory.SubFactory(UserFactory)

class IdeaVoteFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.IdeaVote

    idea = factory.SubFactory(IdeaFactory)
    voter = factory.SubFactory(UserFactory)
    type = factory.Faker('boolean')

class NotificationFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.Notification

    sender = factory.SubFactory(UserFactory)
    receiver = factory.SubFactory(UserFactory)
    message = factory.Faker('paragraph')
    time_sent = factory.Faker('date_time_this_year')
    opened = factory.Faker('boolean')

class ProjectFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.Project

    name = factory.Faker('company')
    manager = factory.SubFactory(UserFactory)
    project_status = factory.Iterator(['open', 'closed', 'complete'])
    projection_open = factory.Faker('date_time_this_year')
    project_closed = None
    project_completion = None

    @factory.post_generation
    def set_dates(self, create, extracted, **kwargs):
        if self.project_status == 'closed':
            self.project_closed = self.projection_open + timedelta(days=random.randint(1, 30))
        elif self.project_status == 'complete':
            self.project_completion = self.projection_open + timedelta(days=random.randint(1, 30))

class SkillFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.Skill

    name = factory.Faker('job')
    picture = factory.LazyAttribute(lambda _: f"https://example.com/images/{fake.uuid4()}.jpg")
    category = factory.SubFactory(SkillCategoryFactory)

class UserBusinessStrengthFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.UserBusinessStrength

    user = factory.SubFactory(UserFactory)
    strength = factory.SubFactory(BusinessStrengthFactory)

class UserDailyActivityProgressFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.UserDailyActivityProgress

    user = factory.SubFactory(UserFactory)
    activity = factory.SubFactory(DailyActivityFactory)
    date = factory.Faker('date_this_year')
    progress = factory.LazyAttribute(lambda _: random.randint(0, 100))

class UserPostFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.UserPost

    title = factory.Faker('sentence')
    content = factory.Faker('text')
    thumbnail = factory.LazyAttribute(lambda _: f"https://example.com/images/{fake.uuid4()}.jpg")
    video_url = factory.LazyAttribute(lambda _: f"https://example.com/videos/{fake.uuid4()}")
    published = True
    poster = factory.SubFactory(UserFactory)

class UserStrengthFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.UserStrength

    user = factory.SubFactory(UserFactory)
    strength = factory.SubFactory(StrengthFactory)

class UserSubscriptionFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.UserSubscription

    user = factory.SubFactory(UserFactory)
    subscription = factory.SubFactory(SubscriptionFactory)
    date_from = factory.Faker('date_time_this_year')
    date_to = factory.LazyAttribute(lambda o: o.date_from + timedelta(days=o.subscription.valid_days))
    price = factory.LazyAttribute(lambda o: o.subscription.price)
    total = factory.LazyAttribute(lambda o: o.subscription.price)
    tax_amount = 0
    tax_rate = 0
    trial_from = None
    trial_to = None

class ConnectionMastermindRoleFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.ConnectionMastermindRole

    connection = factory.SubFactory(BusinessConnectionFactory)
    role = factory.SubFactory(MastermindRoleFactory)

class ProjectBusinessCategoryFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.ProjectBusinessCategory

    project = factory.SubFactory(ProjectFactory)
    category = factory.SubFactory(BusinessCategoryFactory)

class ProjectRegionFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.ProjectRegion

    project = factory.SubFactory(ProjectFactory)
    region = factory.LazyFunction(
        lambda: ProjectRegionFactory._meta.sqlalchemy_session.query(models.Region).order_by(func.random()).first()
    )

class ProjectBusinessSkillFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.ProjectBusinessSkill

    project = factory.SubFactory(ProjectFactory)
    skill = factory.SubFactory(BusinessSkillFactory)

class UserSkillFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.UserSkill

    user = factory.SubFactory(UserFactory)
    skill = factory.SubFactory(SkillFactory)
