import os
import random
import factory
import factories
import models
import pytz

from datetime import timedelta
from factory.alchemy import SQLAlchemyModelFactory
from faker import Faker
from sqlalchemy import func, not_


fake = Faker("en_AU")
AEST = pytz.timezone("Australia/Brisbane")

business_data = {
    "SaaS": {
        "names": [
            "NexusFlow",
            "DataStream",
            "ConnectSphere",
            "QuantumLeap AI",
            "InnovateCloud",
            "SynthWave Analytics",
        ],
        "taglines": [
            "Integrating Your World",
            "The Future of Data, Today",
            "Seamless Collaboration",
            "AI-Powered Insights",
        ],
    },
    "E-commerce": {
        "names": [
            "The Local Pantry",
            "Outback Gear Co.",
            "Coastal Threads",
            "Artisan Alley",
            "EcoEssentials",
        ],
        "taglines": [
            "Fresh & Local, Delivered",
            "Adventure Awaits",
            "Beach-Inspired Fashion",
            "Handcrafted Goods",
        ],
    },
    "Consulting": {
        "names": [
            "Momentum Strategy Group",
            "Apex Financial Solutions",
            "BlueGum Digital Marketing",
            "Ironbark Security",
        ],
        "taglines": [
            "Driving Growth & Innovation",
            "Your Financial Partner",
            "Digital Presence, Perfected",
            "Securing Your Future",
        ],
    },
    "Manufacturing": {
        "names": [
            "Precision Components Pty Ltd",
            "Sun-Kissed Foods",
            "TerraForm Robotics",
            "EcoPack Solutions",
        ],
        "taglines": [
            "Engineered for Excellence",
            "Quality Ingredients, Honest Food",
            "Automating Tomorrow",
            "Sustainable Packaging",
        ],
    },
}

project_names = [
    "Project Phoenix: UI/UX Overhaul",
    "API Integration Gateway",
    "Predictive Analytics Engine",
    "Natural Language Processing Bot",
    'Q4 "Summer Campaign" Launch',
    "SEO Content Strategy Revamp",
    "Winter 2026 Collection Launch",
    "E-commerce Platform Migration",
]

post_content = [
    {
        "title": "The Future of Remote Work",
        "content": "Just read a fascinating report on hybrid work models. It seems flexibility is no longer a perk, but a core expectation. How has your company adapted?",
    },
    {
        "title": "Excited to be at the Brisbane Tech Summit!",
        "content": "Looking forward to connecting with other innovators and learning about the latest trends in AI and cloud computing. DM me if you want to connect!",
    },
    {
        "title": "5 Tips for Effective Leadership",
        "content": "1. Listen more than you speak. 2. Empower your team. 3. Be transparent. 4. Lead with empathy. 5. Never stop learning. What would you add?",
    },
    {
        "title": "Celebrating a huge milestone!",
        "content": "Thrilled to announce that our team has just onboarded our 1000th customer! So proud of everyone's hard work and dedication.",
    },
]

idea_list = [
    "A platform that connects local farmers directly with restaurants to reduce food waste.",
    "An AI-powered tool for small businesses to automate their social media marketing.",
    "A subscription box service for Australian-made, eco-friendly home products.",
    "A virtual reality training platform for high-risk professions like mining and construction.",
    "A mobile app that uses gamification to teach financial literacy to young adults.",
]

SKILL_LIST = [
    "Python",
    "JavaScript",
    "React.js",
    "Node.js",
    "SQL",
    "NoSQL",
    "MongoDB",
    "PostgreSQL",
    "Cloud Computing",
    "AWS",
    "Azure",
    "Google Cloud Platform",
    "Docker",
    "Kubernetes",
    "CI/CD",
    "Git",
    "Agile Methodologies",
    "Scrum",
    "Project Management",
    "Product Management",
    "Data Analysis",
    "Machine Learning",
    "TensorFlow",
    "PyTorch",
    "Natural Language Processing",
    "Financial Modeling",
    "Market Research",
    "Business Strategy",
    "Venture Capital",
    "Digital Marketing",
    "SEO",
    "SEM",
    "Content Strategy",
    "Google Analytics",
    "Social Media Management",
    "UI/UX Design",
    "Figma",
    "Adobe XD",
    "User Research",
    "Cybersecurity",
    "Penetration Testing",
]

BUSINESS_SKILL_LIST = [
    "Strategic Planning",
    "Digital Marketing",
    "SEO/SEM",
    "Content Marketing",
    "Sales Funnel Optimization",
    "Lead Generation",
    "CRM Management",
    "Financial Modeling",
    "Venture Capital Fundraising",
    "Operations Management",
    "Supply Chain Logistics",
    "Product Management",
    "Agile Methodologies",
    "User Experience (UX) Design",
    "User Interface (UI) Design",
    "Cybersecurity Consulting",
    "Cloud Architecture (AWS/Azure/GCP)",
    "B2B Sales",
    "Go-to-Market Strategy",
]


# ===================================================================
# CORE ENTITY FACTORIES
# ===================================================================
class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.User
        sqlalchemy_session_persistence = "flush"

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    contact_email = factory.LazyAttribute(
        lambda o: f"{o.first_name.lower()}.{o.last_name.lower()}@example.com"
    )
    contact_phone_no = factory.LazyFunction(
        lambda: f"04{random.randint(10000000, 99999999)}"
    )


class BusinessCategoryFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.BusinessCategory
        sqlalchemy_session_persistence = "flush"
        sqlalchemy_get_or_create = ("name",)

    name = factory.Faker("bs")


class BusinessPhaseFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.BusinessPhase
        sqlalchemy_session_persistence = "flush"
        sqlalchemy_get_or_create = ("name",)

    name = factory.Iterator(["Startup", "Growth", "Mature", "Decline"])


class BusinessRoleFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.BusinessRole
        sqlalchemy_session_persistence = "flush"
        sqlalchemy_get_or_create = ("name",)

    name = factory.Iterator(["Founder", "Investor", "Advisor", "Employee"])


class BusinessSkillFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.BusinessSkill
        sqlalchemy_session_persistence = "flush"
        sqlalchemy_get_or_create = ("name",)

    name = factory.Iterator(BUSINESS_SKILL_LIST)


class BusinessTypeFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.BusinessType
        sqlalchemy_session_persistence = "flush"
        sqlalchemy_get_or_create = ("name",)

    name = factory.Iterator(["SaaS", "E-commerce", "Consulting", "Manufacturing"])


class IdeaFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.Idea
        sqlalchemy_session_persistence = "flush"

    content = factory.Iterator(idea_list)
    submitter = factory.SubFactory(UserFactory)


# ===================================================================
# HELPER FUNCTIONS
# ===================================================================
def get_random(model, exclude=None):
    """Helper function to get a random instance of a model from the DB with optional exclusion."""
    session = UserFactory._meta.sqlalchemy_session
    if session:
        query = session.query(model)
        if query.count() > 0:
            if exclude:
                query = query.filter(not_(exclude))
            return query.order_by(func.random()).first()
    return None


def get_complementary_business(session, base_business):
    """Finds a business that is a good complementary partner."""
    if not base_business or not base_business.business_type:
        return None

    complementary_partner = (
        session.query(models.Business)
        .filter(
            models.Business.id != base_business.id,
            models.Business.business_type_id == base_business.business_type_id,
            models.Business.business_category_id != base_business.business_category_id,
        )
        .order_by(func.random())
        .first()
    )
    return complementary_partner


# ===================================================================
# DEPENDENT FACTORIES
# ===================================================================
class BusinessFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.Business
        sqlalchemy_session_persistence = "flush"

    operator = factory.SubFactory(UserFactory)
    business_type = factory.LazyFunction(lambda: get_random(models.BusinessType))
    business_category = factory.LazyFunction(
        lambda: get_random(models.BusinessCategory)
    )

    @factory.lazy_attribute
    def phase(self):
        session = UserFactory._meta.sqlalchemy_session
        if self.business_type.name == "SaaS":
            phase_name = random.choice(["Startup", "Growth"])
        else:
            phase_name = random.choice(["Growth", "Mature"])
        return session.query(models.BusinessPhase).filter_by(name=phase_name).one()

    @factory.lazy_attribute
    def name(self):
        return random.choice(
            business_data.get(self.business_type.name, {}).get(
                "names", ["Generic Business Name"]
            )
        )

    @factory.lazy_attribute
    def tagline(self):
        return random.choice(
            business_data.get(self.business_type.name, {}).get(
                "taglines", ["A Generic Tagline"]
            )
        )

    website = factory.LazyAttribute(
        lambda o: f"https://www.{o.name.replace(' ', '').replace('.', '').lower()}.com.au"
    )
    description = factory.Faker("paragraph", nb_sentences=3)
    address = factory.Faker("street_address")
    city = "Brisbane"


class UserPostFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.UserPost
        sqlalchemy_session_persistence = "flush"

    @factory.lazy_attribute
    def title(self):
        return random.choice(post_content)["title"]

    @factory.lazy_attribute
    def content(self):
        for post in post_content:
            if post["title"] == self.title:
                return post["content"]
        return ""

    thumbnail = factory.LazyAttribute(
        lambda _: f"https://placehold.co/600x400/cccccc/222222?text=Blog+Post"
    )
    video_url = None
    published = True
    poster = factory.SubFactory(UserFactory)


class ProjectFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.Project
        sqlalchemy_session_persistence = "flush"

    name = factory.Iterator(project_names)
    manager = factory.SubFactory(UserFactory)
    project_status = factory.Iterator(["open", "closed", "complete"])
    projection_open = factory.Faker(
        "date_time_between", start_date="-1y", end_date="-1m", tzinfo=AEST
    )
    project_closed = None
    project_completion = None

    @factory.post_generation
    def set_dates(self, create, extracted, **kwargs):
        if self.project_status == "closed":
            self.project_closed = self.projection_open + timedelta(
                days=random.randint(30, 180)
            )
        elif self.project_status == "complete":
            self.project_completion = self.projection_open + timedelta(
                days=random.randint(60, 365)
            )


class SkillCategoryFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.SkillCategory
        sqlalchemy_session_persistence = "flush"

    name = factory.Faker("job")
    business_type = factory.SubFactory(BusinessTypeFactory)


class SkillFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.Skill
        sqlalchemy_session_persistence = "flush"
        sqlalchemy_get_or_create = ("name",)

    name = factory.Iterator(SKILL_LIST)
    picture = None
    category = factory.SubFactory(SkillCategoryFactory)


class UserLoginFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.UserLogin
        sqlalchemy_session_persistence = "flush"

    user = factory.SubFactory(UserFactory)
    login_email = factory.LazyAttribute(lambda o: o.user.contact_email)
    password_hash = factory.LazyAttribute(lambda _: os.urandom(70))
    password_reset_token = None
    password_reset_requested_timestamp = None


class SubscriptionFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.Subscription
        sqlalchemy_session_persistence = "flush"

    name = factory.Iterator(["Basic", "Pro", "Enterprise"])
    price = factory.LazyAttribute(lambda _: round(random.uniform(10, 500), 2))
    valid_days = factory.LazyAttribute(lambda _: random.randint(30, 365))
    valid_months = factory.LazyAttribute(lambda _: random.randint(1, 12))


class UserSubscriptionFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.UserSubscription
        sqlalchemy_session_persistence = "flush"

    user = factory.SubFactory(UserFactory)
    subscription = factory.SubFactory(SubscriptionFactory)
    date_from = factory.Faker("date_time_this_year", tzinfo=AEST)
    date_to = factory.LazyAttribute(
        lambda o: o.date_from + timedelta(days=o.subscription.valid_days)
    )
    price = factory.LazyAttribute(lambda o: o.subscription.price)
    total = factory.LazyAttribute(lambda o: o.subscription.price)
    tax_amount = 0
    tax_rate = 0
    trial_from = None
    trial_to = None


class ConnectionTypeFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.ConnectionType
        sqlalchemy_session_persistence = "flush"
        sqlalchemy_get_or_create = ("name",)

    name = factory.Iterator(["Partnership", "Supplier", "Customer", "Investor"])


class DailyActivityFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.DailyActivity
        sqlalchemy_session_persistence = "flush"

    name = factory.Faker("word")
    description = factory.Faker("sentence")


class IndustryCategoryFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.IndustryCategory
        sqlalchemy_session_persistence = "flush"
        sqlalchemy_get_or_create = ("name",)

    name = factory.Faker("job")


class IndustryFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.Industry
        sqlalchemy_session_persistence = "flush"

    name = factory.Faker("job")
    picture = None
    category = factory.SubFactory(IndustryCategoryFactory)


class MastermindRoleFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.MastermindRole
        sqlalchemy_session_persistence = "flush"
        sqlalchemy_get_or_create = ("name",)

    name = factory.Iterator(["Leader", "Strategist", "Implementer", "Innovator"])


class StrengthCategoryFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.StrengthCategory
        sqlalchemy_session_persistence = "flush"
        sqlalchemy_get_or_create = ("name",)

    name = factory.Iterator(["Technical", "Business", "Creative", "Leadership"])


class StrengthFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.Strength
        sqlalchemy_session_persistence = "flush"

    name = factory.Faker("job")
    category = factory.SubFactory(StrengthCategoryFactory)


class BusinessStrengthFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.BusinessStrength
        sqlalchemy_session_persistence = "flush"

    name = factory.Faker("job")
    role = factory.SubFactory(BusinessRoleFactory)
    phase = factory.SubFactory(BusinessPhaseFactory)


class CaseStudyFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.CaseStudy
        sqlalchemy_session_persistence = "flush"

    title = factory.Faker("sentence")
    content = factory.Faker("text")
    thumbnail = factory.LazyAttribute(
        lambda _: f"https://placehold.co/600x400/cccccc/222222?text=Case+Study"
    )
    video_url = None
    published = True
    owner = factory.SubFactory(UserFactory)


# ===================================================================
# LINKING TABLE FACTORIES
# ===================================================================


class BusinessConnectionFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.BusinessConnection
        sqlalchemy_session_persistence = "flush"

    initiating_business = factory.LazyFunction(lambda: get_random(models.Business))

    @factory.lazy_attribute
    def receiving_business(self):
        session = UserFactory._meta.sqlalchemy_session
        partner = get_complementary_business(session, self.initiating_business)
        return partner or get_random(
            models.Business, exclude=(models.Business.id == self.initiating_business.id)
        )

    connection_type = factory.SubFactory(ConnectionTypeFactory)
    active = True
    date_initiated = factory.Faker(
        "date_time_between", start_date="-2y", end_date="now", tzinfo=AEST
    )


class DailyActivityEnrolmentFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.DailyActivityEnrolment
        sqlalchemy_session_persistence = "flush"
        sqlalchemy_get_or_create = ("activity", "user")

    activity = factory.LazyFunction(lambda: get_random(models.DailyActivity))
    user = factory.LazyFunction(lambda: get_random(models.User))


class IdeaVoteFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.IdeaVote
        sqlalchemy_session_persistence = "flush"
        sqlalchemy_get_or_create = ("voter", "idea")

    idea = factory.LazyFunction(lambda: get_random(models.Idea))
    voter = factory.LazyFunction(lambda: get_random(models.User))
    type = factory.Faker("boolean")


class NotificationFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.Notification
        sqlalchemy_session_persistence = "flush"

    sender = factory.LazyFunction(lambda: get_random(models.User))
    receiver = factory.LazyFunction(lambda: get_random(models.User))
    message = factory.Faker("sentence")
    time_sent = factory.Faker(
        "date_time_between", start_date="-1y", end_date="now", tzinfo=AEST
    )
    opened = factory.Faker("boolean")


class UserSkillFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.UserSkill
        sqlalchemy_session_persistence = "flush"
        sqlalchemy_get_or_create = ("user", "skill")

    user = factory.LazyFunction(lambda: get_random(models.User))
    skill = factory.LazyFunction(
        lambda: get_random(models.Skill) or factories.SkillFactory()
    )


class UserBusinessStrengthFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.UserBusinessStrength
        sqlalchemy_session_persistence = "flush"
        sqlalchemy_get_or_create = ("user", "strength")

    user = factory.LazyFunction(lambda: get_random(models.User))
    strength = factory.SubFactory(BusinessStrengthFactory)


class UserDailyActivityProgressFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.UserDailyActivityProgress
        sqlalchemy_session_persistence = "flush"

    user = factory.LazyFunction(lambda: get_random(models.User))
    activity = factory.LazyFunction(lambda: get_random(models.DailyActivity))
    date = factory.Faker("date_this_year")
    progress = factory.LazyAttribute(lambda _: random.randint(0, 100))


class UserStrengthFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.UserStrength
        sqlalchemy_session_persistence = "flush"
        sqlalchemy_get_or_create = ("user", "strength")

    user = factory.LazyFunction(lambda: get_random(models.User))
    strength = factory.SubFactory(StrengthFactory)


class ConnectionMastermindRoleFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.ConnectionMastermindRole
        sqlalchemy_session_persistence = "flush"
        sqlalchemy_get_or_create = ("connection", "role")

    connection = factory.LazyFunction(lambda: get_random(models.BusinessConnection))
    role = factory.LazyFunction(lambda: get_random(models.MastermindRole))


class ProjectBusinessCategoryFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.ProjectBusinessCategory
        sqlalchemy_session_persistence = "flush"
        sqlalchemy_get_or_create = ("project", "category")

    project = factory.LazyFunction(lambda: get_random(models.Project))
    category = factory.LazyFunction(lambda: get_random(models.BusinessCategory))


class ProjectRegionFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.ProjectRegion
        sqlalchemy_session_persistence = "flush"
        sqlalchemy_get_or_create = ("project", "region")

    project = factory.LazyFunction(lambda: get_random(models.Project))
    region = factory.LazyFunction(lambda: get_random(models.Region))


class ProjectBusinessSkillFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.ProjectBusinessSkill
        sqlalchemy_session_persistence = "flush"
        sqlalchemy_get_or_create = ("project", "skill")

    project = factory.LazyFunction(lambda: get_random(models.Project))
    skill = factory.LazyFunction(lambda: get_random(models.BusinessSkill))
