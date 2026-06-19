
from flask import Blueprint, render_template
from src.database.models import ComplianceResult

compliance_bp = Blueprint('compliance', __name__, url_prefix='/compliance')

@compliance_bp.route('/')
def benchmarks():
    """View compliance benchmarks."""
    results = ComplianceResult.query.all()
    return render_template('compliance/benchmark_report.html', results=results)

@compliance_bp.route('/<int:result_id>')
def view_benchmark(result_id):
    """View a specific benchmark result."""
    result = ComplianceResult.query.get_or_404(result_id)
    return render_template('compliance/benchmark_report.html', result=result)
