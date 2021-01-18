import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from Utils.ElementUtil.Element import Element
import allure


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    """
    Extends the PyTest Plugin to take and embed screenshot in html report, whenever test fails.
    :param item:
    """
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])
    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        # 判断用例是否失败或者xfail跳过的测试
        if (report.skipped and xfail) or (report.failed and not xfail):
            # 获取测试用例代码中webDriver参数来获取浏览器进行抓屏
            # for i in item.funcargs:
            #     if isinstance(item.funcargs[i], WebDriver):
            #         # 截图
            #         # basic.save_capture(item.funcargs[i], "异常截图")
            #         pass
            #     pass
            # 获取el对象截图，并附加到allure报告中
            if hasattr(item.instance, 'el'):
                if isinstance(item.instance.el, Element):
                    print('截图')
                    img = item.instance.el.catch_screen_as_png(dpi=item.instance.dpi)
                    allure.attach(img, '失败自动截图', allure.attachment_type.PNG)
            pass
        report.extra = extra


def pytest_addoption(parser):
    parser.addoption(
        "--dsrange", action="store", default="all", help="data source range: 1-3 or 1,3,4 or all"
    )


@pytest.fixture
def dsrange(request):
    return request.config.getoption("--dsrange")

