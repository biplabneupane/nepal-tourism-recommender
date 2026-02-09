"""
Database models for Nepal Tourism Recommender
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()


class UserPreference(db.Model):
    """Store user preferences for personalization"""
    __tablename__ = 'user_preferences'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), index=True)  # Anonymous session identifier
    user_email = db.Column(db.String(255), index=True, nullable=True)  # Optional email
    
    # Preference fields
    preferred_category = db.Column(db.String(100))
    max_cost = db.Column(db.Float)
    difficulty = db.Column(db.String(50))
    preferred_regions = db.Column(db.Text)  # JSON array of regions
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    visit_count = db.Column(db.Integer, default=1)
    
    def to_dict(self):
        return {
            'id': self.id,
            'session_id': self.session_id,
            'preferred_category': self.preferred_category,
            'max_cost': self.max_cost,
            'difficulty': self.difficulty,
            'preferred_regions': json.loads(self.preferred_regions) if self.preferred_regions else [],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'visit_count': self.visit_count
        }


class Lead(db.Model):
    """Store conversion leads"""
    __tablename__ = 'leads'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Contact information
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, index=True)
    phone = db.Column(db.String(50), nullable=True)
    
    # Lead type
    lead_type = db.Column(db.String(50), nullable=False)  # 'email', 'expert', 'quote'
    
    # Related attractions (JSON array of attraction IDs)
    attraction_ids = db.Column(db.Text, nullable=True)
    
    # Additional data (JSON)
    lead_metadata = db.Column(db.Text, nullable=True)  # For storing extra info like itinerary days, etc.
    
    # Status tracking
    status = db.Column(db.String(50), default='new')  # 'new', 'contacted', 'converted', 'lost'
    notes = db.Column(db.Text, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    contacted_at = db.Column(db.DateTime, nullable=True)
    
    # Email tracking
    email_sent = db.Column(db.Boolean, default=False)
    email_sent_at = db.Column(db.DateTime, nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'lead_type': self.lead_type,
            'attraction_ids': json.loads(self.attraction_ids) if self.attraction_ids else [],
            'lead_metadata': json.loads(self.lead_metadata) if self.lead_metadata else {},
            'status': self.status,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'email_sent': self.email_sent
        }


class ConversionRequest(db.Model):
    """Track conversion requests and email sends"""
    __tablename__ = 'conversion_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    lead_id = db.Column(db.Integer, db.ForeignKey('leads.id'), nullable=True)
    
    request_type = db.Column(db.String(50), nullable=False)  # 'email', 'expert', 'quote'
    email_to = db.Column(db.String(255), nullable=False)
    
    # Email content
    subject = db.Column(db.String(500))
    body = db.Column(db.Text)
    
    # Status
    status = db.Column(db.String(50), default='pending')  # 'pending', 'sent', 'failed'
    error_message = db.Column(db.Text, nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    sent_at = db.Column(db.DateTime, nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'lead_id': self.lead_id,
            'request_type': self.request_type,
            'email_to': self.email_to,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'sent_at': self.sent_at.isoformat() if self.sent_at else None
        }


class Analytics(db.Model):
    """Store analytics data for recommendations"""
    __tablename__ = 'analytics'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), index=True)
    
    # Recommendation context
    recommendation_type = db.Column(db.String(50))  # 'similar', 'preferences', 'browse'
    attraction_id = db.Column(db.Integer, index=True)
    clicked = db.Column(db.Boolean, default=False)
    converted = db.Column(db.Boolean, default=False)
    
    # User preferences at time of recommendation
    user_preferences = db.Column(db.Text)  # JSON
    
    # Timestamp
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'session_id': self.session_id,
            'recommendation_type': self.recommendation_type,
            'attraction_id': self.attraction_id,
            'clicked': self.clicked,
            'converted': self.converted,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
