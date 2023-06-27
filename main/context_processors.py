from .forms import ReportProblemForm

def report_problem_form(request):
    return {'report_problem_form': ReportProblemForm()}
