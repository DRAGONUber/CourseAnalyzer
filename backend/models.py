from app import db

class GradeDistribution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    term = db.Column(db.String(50), nullable=False)
    year = db.Column(db.String(4), nullable=False)
    course_subject = db.Column(db.String(10), nullable=False)
    course_number = db.Column(db.String(10), nullable=False)
    instructor = db.Column(db.String(100), nullable=False)
    grade_a = db.Column(db.Integer)
    grade_b = db.Column(db.Integer)
    grade_c = db.Column(db.Integer)
    grade_d = db.Column(db.Integer)
    grade_f = db.Column(db.Integer)
