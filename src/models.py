from sqlalchemy import BINARY as Binary
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy import (
    Column, Integer, String, ForeignKey, DECIMAL, Text, Date,
    DateTime, Boolean, Enum, LargeBinary, CHAR
)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(60))
    last_name = Column(String(60))
    contact_email = Column(String(254))
    contact_phone_no = Column(String(10))


class BusinessCategory(Base):
    __tablename__ = 'business_categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))


class BusinessPhase(Base):
    __tablename__ = 'business_phases'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))


class BusinessRole(Base):
    __tablename__ = 'business_roles'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))


class BusinessSkill(Base):
    __tablename__ = 'business_skills'
    # UPDATED: Let the database handle the primary key generation. Added unique constraint.
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(60), unique=True)


class BusinessType(Base):
    __tablename__ = 'business_types'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))


class ConnectionType(Base):
    __tablename__ = 'connection_types'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))


class DailyActivity(Base):
    __tablename__ = 'daily_activities'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(60))
    description = Column(Text)


class IndustryCategory(Base):
    __tablename__ = 'industry_categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))


class MastermindRole(Base):
    __tablename__ = 'mastermind_roles'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))


class Region(Base):
    __tablename__ = 'regions'
    id = Column(CHAR(3), primary_key=True)  # 3-letter country code
    name = Column(String(100))  # Full country name


class StrengthCategory(Base):
    __tablename__ = 'strength_categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))


class Subscription(Base):
    __tablename__ = 'subscriptions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(45))
    price = Column(DECIMAL(16, 2))
    valid_days = Column(Integer)
    valid_months = Column(Integer)


class Business(Base):
    __tablename__ = 'businesses'
    id = Column(Integer, primary_key=True, autoincrement=True)
    operator_user_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String(100))
    tagline = Column(String(100))
    website = Column(String(255))
    description = Column(Text)
    address = Column(String(100))
    city = Column(String(60))
    business_type_id = Column(Integer, ForeignKey('business_types.id'))
    business_category_id = Column(
        Integer, ForeignKey('business_categories.id'))
    business_phase = Column(Integer, ForeignKey('business_phases.id'))

    operator = relationship("User")
    business_type = relationship("BusinessType")
    business_category = relationship("BusinessCategory")
    phase = relationship("BusinessPhase")


class BusinessStrength(Base):
    __tablename__ = 'business_strengths'
    id = Column(Integer, primary_key=True, autoincrement=True)
    business_role_id = Column(Integer, ForeignKey('business_roles.id'))
    business_phase_id = Column(Integer, ForeignKey('business_phases.id'))
    name = Column(String(100))

    role = relationship("BusinessRole")
    phase = relationship("BusinessPhase")


class CaseStudy(Base):
    __tablename__ = 'case_studies'
    id = Column(Integer, primary_key=True, autoincrement=True)
    owner_user_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String(255))
    content = Column(Text)
    thumbnail = Column(String(255))
    video_url = Column(String(255))
    published = Column(Boolean)

    owner = relationship("User")


class Idea(Base):
    __tablename__ = 'ideas'
    # UPDATED: Let the database handle the primary key generation.
    id = Column(Integer, primary_key=True, autoincrement=True)
    submitted_by_user_id = Column(Integer, ForeignKey('users.id'))
    content = Column(Text)

    submitter = relationship("User")


class Industry(Base):
    __tablename__ = 'industries'
    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey('industry_categories.id'))
    name = Column(String(100))
    picture = Column(String(255))

    category = relationship("IndustryCategory")


class SkillCategory(Base):
    __tablename__ = 'skill_categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    business_type_id = Column(Integer, ForeignKey('business_types.id'))

    business_type = relationship("BusinessType")


class Strength(Base):
    __tablename__ = 'strengths'
    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey('strength_categories.id'))
    name = Column(String(100))

    category = relationship("StrengthCategory")


class UserLogin(Base):
    __tablename__ = 'user_logins'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    login_email = Column(String(254))
    password_hash = Column(Binary(70))
    password_reset_token = Column(LargeBinary)
    password_reset_requested_timestamp = Column(DateTime)

    user = relationship("User")


class BusinessConnection(Base):
    __tablename__ = 'business_connections'
    id = Column(Integer, primary_key=True, autoincrement=True)
    initiating_business_id = Column(Integer, ForeignKey('businesses.id'))
    receiving_business_id = Column(Integer, ForeignKey('businesses.id'))
    connection_type_id = Column(Integer, ForeignKey('connection_types.id'))
    active = Column(Boolean)
    date_initiated = Column(DateTime)

    initiating_business = relationship(
        "Business", foreign_keys=[initiating_business_id])
    receiving_business = relationship(
        "Business", foreign_keys=[receiving_business_id])
    connection_type = relationship("ConnectionType")


class DailyActivityEnrolment(Base):
    __tablename__ = 'daily_activity_enrolments'
    daily_activity_id = Column(Integer, ForeignKey(
        'daily_activities.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)

    activity = relationship("DailyActivity")
    user = relationship("User")


class IdeaVote(Base):
    __tablename__ = 'idea_votes'
    voter_user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    idea_id = Column(Integer, ForeignKey('ideas.id'), primary_key=True)
    type = Column(Boolean)

    voter = relationship("User")
    idea = relationship("Idea")


class Notification(Base):
    __tablename__ = 'notifications'
    id = Column(Integer, primary_key=True, autoincrement=True)
    sender_user_id = Column(Integer, ForeignKey('users.id'))
    receiver_user_id = Column(Integer, ForeignKey('users.id'))
    message = Column(Text)
    time_sent = Column(DateTime)
    opened = Column(Boolean)

    sender = relationship("User", foreign_keys=[sender_user_id])
    receiver = relationship("User", foreign_keys=[receiver_user_id])


class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True, autoincrement=True)
    managed_by_user_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String(100))
    project_status = Column(Enum('open', 'closed', 'complete'))
    projection_open = Column(DateTime)
    project_closed = Column(DateTime)
    project_completion = Column(DateTime)

    manager = relationship("User")


class Skill(Base):
    __tablename__ = 'skills'
    id = Column(Integer, primary_key=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey('skill_categories.id'))
    name = Column(String(100))
    picture = Column(String(255))

    category = relationship("SkillCategory")


class UserBusinessStrength(Base):
    __tablename__ = 'user_business_strengths'
    business_strength_id = Column(Integer, ForeignKey(
        'business_strengths.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)

    strength = relationship("BusinessStrength")
    user = relationship("User")


class UserDailyActivityProgress(Base):
    __tablename__ = 'user_daily_activity_progress'
    date = Column(Date, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    daily_activity_id = Column(Integer, ForeignKey(
        'daily_activities.id'), primary_key=True)
    progress = Column(Integer)

    user = relationship("User")
    activity = relationship("DailyActivity")


class UserPost(Base):
    __tablename__ = 'user_posts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    poster_user_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String(255))
    content = Column(Text)
    thumbnail = Column(String(255))
    video_url = Column(String(255))
    published = Column(Boolean)

    poster = relationship("User")


class UserStrength(Base):
    __tablename__ = 'user_strengths'
    strength_id = Column(Integer, ForeignKey('strengths.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)

    strength = relationship("Strength")
    user = relationship("User")


class UserSubscription(Base):
    __tablename__ = 'user_subscriptions'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    subscription_id = Column(Integer, ForeignKey(
        'subscriptions.id'), primary_key=True)
    date_from = Column(DateTime)
    date_to = Column(DateTime)
    price = Column(DECIMAL(16, 2))
    total = Column(DECIMAL(16, 2))
    tax_amount = Column(DECIMAL(16, 2))
    tax_rate = Column(DECIMAL(6, 3))
    trial_from = Column(DateTime)
    trial_to = Column(DateTime)

    user = relationship("User")
    subscription = relationship("Subscription")


class ConnectionMastermindRole(Base):
    __tablename__ = 'connection_mastermind_roles'
    connection_id = Column(Integer, ForeignKey(
        'business_connections.id'), primary_key=True)
    mastermind_role_id = Column(Integer, ForeignKey(
        'mastermind_roles.id'), primary_key=True)

    connection = relationship("BusinessConnection")
    role = relationship("MastermindRole")


class ProjectBusinessCategory(Base):
    __tablename__ = 'project_business_categories'
    project_id = Column(Integer, ForeignKey('projects.id'), primary_key=True)
    business_category_id = Column(Integer, ForeignKey(
        'business_categories.id'), primary_key=True)

    project = relationship("Project")
    category = relationship("BusinessCategory")


class ProjectBusinessSkill(Base):
    __tablename__ = 'project_business_skills'
    project_id = Column(Integer, ForeignKey('projects.id'), primary_key=True)
    business_skill_id = Column(Integer, ForeignKey(
        'business_skills.id'), primary_key=True)

    project = relationship("Project")
    skill = relationship("BusinessSkill")


class ProjectRegion(Base):
    __tablename__ = 'project_regions'
    region_id = Column(CHAR(3), ForeignKey('regions.id'), primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'), primary_key=True)

    region = relationship("Region")
    project = relationship("Project")


class UserSkill(Base):
    __tablename__ = 'user_skills'
    skill_id = Column(Integer, ForeignKey('skills.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)

    skill = relationship("Skill")
    user = relationship("User")
