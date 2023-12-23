from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://channels.weixin.qq.com/platform/post/list")
    page.goto("https://channels.weixin.qq.com/login.html")
    page.goto("https://channels.weixin.qq.com/platform/post/list")
    page.get_by_role("button", name="发表视频").click()
    page.get_by_role("button", name="上传时长2小时内，大小不超过4GB，建议分辨率720p及以上，码率10Mbps以内，格式为MP4/H.264格式").click()
    page.get_by_role("button", name="上传时长2小时内，大小不超过4GB，建议分辨率720p及以上，码率10Mbps以内，格式为MP4/H.264格式").set_input_files("WeChat_20231210084509.mp4")
    page.get_by_role("button", name="上传时长2小时内，大小不超过4GB，建议分辨率720p及以上，码率10Mbps以内，格式为MP4/H.264格式").click()
    page.get_by_role("button", name="上传时长2小时内，大小不超过4GB，建议分辨率720p及以上，码率10Mbps以内，格式为MP4/H.264格式").set_input_files("WeChat_20231210084509.mp4")
    page.get_by_role("button", name="上传时长2小时内，大小不超过4GB，建议分辨率720p及以上，码率10Mbps以内，格式为MP4/H.264格式").click()
    page.get_by_role("button", name="上传时长2小时内，大小不超过4GB，建议分辨率720p及以上，码率10Mbps以内，格式为MP4/H.264格式").set_input_files("普通话第三节课：韵母的滑动.mp4")
    page.locator(".input-editor").fill("1")
    page.locator(".input-editor").click()
    page.get_by_text("1", exact=True).fill("111")
    page.get_by_placeholder("概括视频主要内容，字数建议6-16个字符").click()
    page.get_by_placeholder("概括视频主要内容，字数建议6-16个字符").fill("2222")
    page.get_by_role("button", name="发表").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)