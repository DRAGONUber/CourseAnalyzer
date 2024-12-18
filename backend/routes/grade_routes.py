from flask import Blueprint, jsonify, request
from models import GradeDistribution

grade_routes = Blueprint('grades', __name__)

@grade_routes.route('/grades', methods=['GET'])
def get_grades():
    term = request.args.get('term')
    year = request.args.get('year')
    instructor = request.args.get('instructor')
    course = request.args.get('course')

    query = GradeDistribution.query
    if term:
        query = query.filter_by(term=term)
    if year:
        query = query.filter_by(year=year)
    if instructor:
        query = query.filter(GradeDistribution.instructor.ilike(f"%{instructor}%"))
    if course:
        query = query.filter(GradeDistribution.course_subject.ilike(f"%{course}%"))

    grades = query.all()
    result = [{"id": g.id, "term": g.term, "year": g.year, "course": f"{g.course_subject} {g.course_number}", "instructor": g.instructor} for g in grades]

    return jsonify(result)
