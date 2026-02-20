
import os
from playwright.sync_api import sync_playwright

def verify_responsive():
    cwd = os.getcwd()
    files = ['student_dashboard.html', 'analytics.html', 'dash.html']

    with sync_playwright() as p:
        browser = p.chromium.launch()

        for filename in files:
            page = browser.new_page()
            url = f"file://{cwd}/{filename}"
            print(f"Checking {url}")

            # 1. Desktop View
            page.set_viewport_size({"width": 1280, "height": 800})
            page.goto(url)
            page.wait_for_timeout(1000) # Wait for animations/Alpine
            page.screenshot(path=f"verification/{filename.replace('.html', '_desktop.png')}")
            print(f"Captured desktop screenshot for {filename}")

            # 2. Mobile View (Sidebar closed)
            page.set_viewport_size({"width": 375, "height": 667})
            page.reload() # Reload to ensure fresh state
            page.wait_for_timeout(1000)
            page.screenshot(path=f"verification/{filename.replace('.html', '_mobile_closed.png')}")
            print(f"Captured mobile closed screenshot for {filename}")

            # 3. Mobile View (Sidebar open)
            # Click the toggle button.
            # For student_dashboard.html, toggle button is in header, but we need to find it.
            # It has logic `sidebarOpen = true`.
            # In analytics and dash, it has id `sidebar-toggle`.

            try:
                if filename == 'student_dashboard.html':
                    # Find button with menu icon or visible on mobile
                    # In my edit: <button @click="sidebarOpen = true" class="lg:hidden ...">
                    # It has a lucide icon "menu".
                    # Let's try to find a button visible on mobile in header.
                    # Or click by selector if specific.
                    # The button I added has `lg:hidden` and is in header.
                    # I'll try to find it by the icon or generic button in header.
                    toggle_btn = page.locator('header button.lg\\:hidden').first
                    if toggle_btn.is_visible():
                        toggle_btn.click()
                    else:
                        print(f"Toggle button not visible for {filename}")
                else:
                    # analytics and dash have id="sidebar-toggle"
                    page.locator('#sidebar-toggle').click()

                page.wait_for_timeout(1000) # Wait for transition
                page.screenshot(path=f"verification/{filename.replace('.html', '_mobile_open.png')}")
                print(f"Captured mobile open screenshot for {filename}")

            except Exception as e:
                print(f"Error toggling sidebar for {filename}: {e}")

        browser.close()

if __name__ == "__main__":
    verify_responsive()
