import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from pathlib import Path
import os


def _require_env(name: str) -> str:
    """Fail fast when mandatory OrangeHRM config is missing."""
    value = os.getenv(name)
    if not value:
        raise pytest.UsageError(f"Missing required environment variable: {name}")
    return value


@pytest.fixture(scope="session")
def orangehrm_base_url():
    """Provide OrangeHRM base URL without trailing slash for route joins."""
    return _require_env("ORANGEHRM_BASE_URL").rstrip("/")


@pytest.fixture(scope="session")
def orangehrm_valid_credentials():
    """Provide known-good credentials for successful authentication checks."""
    username = _require_env("ORANGEHRM_USERNAME")
    password = _require_env("ORANGEHRM_PASSWORD")
    return username, password


@pytest.fixture(scope="session")
def orangehrm_invalid_credentials():
    """Provide an intentionally invalid password for negative auth scenarios."""
    username = _require_env("ORANGEHRM_USERNAME")
    invalid_password = os.getenv("ORANGEHRM_INVALID_PASSWORD", "invalid_password")
    return username, invalid_password

@pytest.fixture
def driver():
    """Create a headless Chrome instance suitable for local and CI runs."""
    options = webdriver.ChromeOptions()
    
    # ✅ Headless & CI-safe options
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")           # required on some Linux/Docker envs
    options.add_argument("--window-size=1920,1080")  # explicit viewport; --start-maximized is a no-op in headless

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    yield driver
    driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach screenshot path to pytest report for any failed UI test."""
    outcome = yield
    report = outcome.get_result()

    if report.when != "call" or report.passed:
        return

    driver_instance = item.funcargs.get("driver")
    if not driver_instance:
        return

    screenshots_dir = Path("artifacts") / "screenshots"
    screenshots_dir.mkdir(parents=True, exist_ok=True)

    safe_name = item.nodeid.replace("::", "__").replace("/", "_").replace("\\", "_")
    screenshot_path = screenshots_dir / f"{safe_name}.png"
    driver_instance.save_screenshot(str(screenshot_path))

    report.sections.append(("screenshot", f"Saved screenshot: {screenshot_path}"))
