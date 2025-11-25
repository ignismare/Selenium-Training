import pytest, pytest_html, datetime
from pytest_metadata.plugin import metadata_key

#change report title
def pytest_html_report_title(report):
    report.title = "Pytest Tutorial Report"

#add project to metadata
def pytest_configure(config):
    config.stash[metadata_key]["Project"] = "Internal: Selenium/Playwright"

def pytest_html_results_table_header(cells):
    cells.insert(3, "<th>Results</th>")
    cells.insert(2, "<th>Description</th>")
    cells.insert(1, '<th class="sortable time" data-column-type="time">Time</th>')

def pytest_html_results_table_row(report, cells):
    cells.insert(3, f"<td>{report.results}</td>")
    cells.insert(2, f"<td>{report.description}</td>")
    cells.insert(1, f'<td class="col-time">{datetime.time}</td>')

def pytest_addoption(parser):
    parser.addoption("--headless", action="store", default=False)

@pytest.fixture
def headless(request):
    return request.config.getoption("--headless")

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    report.description = str(item.function.__doc__)
    report.results = str(item.function.results)
    extras = getattr(report, "extras", [])
    if report.when == "call":
        # always add url to report
        extras.append(pytest_html.extras.url(item.function.site))
        xfail = hasattr(report, "wasxfail")
        if (report.skipped and xfail) or (report.failed and not xfail):
            # only add additional html on failure
            extras.append(pytest_html.extras.html("<div>TEST FAILED</div>"))
        report.extras = extras
