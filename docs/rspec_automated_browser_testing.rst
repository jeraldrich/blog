Headless Browser Testing with Chrome and Rspec
==============================================

If a user can have many different roles and permissions, you'll want to test what they can view for each page.
You can write request specs to test api responses, but this test your view logic.

For testing user flow conditions, I like to simulate what the user will see by driving a chrome browser for each condition.
In this example, I will be using rspec and ruby on rails.

First, let's add these gems to your gemfile::

        gem 'rspec-rails'
        gem 'capybara'
        gem 'capybara-email'
        gem 'webdrivers'

Now create a new directory at spec/support. I like keep all of my test configuration and helper methods here.
Add this line to your rails_helper file to load all of your test support files::

        Dir[Rails.root.join('spec/support/**/*.rb')].each { |f| require f }

Now we will want to configure capybara to work with chrome. Create a new file in spec/support called chrome_setup.rb with this code::

        Capybara.register_driver :selenium_chrome do |app|
          # Set chrome download dir and auto confirm all "are you sure you want to download" to test downloading docs and pdfs.
          chrome_prefs = {
            'download' => {
              'default_directory' => DownloadHelpers::PATH.to_s,
              'prompt_for_download' => false
            },
            'profile' => {
              'default_content_settings' => { 'multiple-automatic-downloads': 1 }, # for chrome version olde ~42
              'default_content_setting_values' => { 'automatic_downloads': 1 }, # for chrome newe 46
              'password_manager_enabled' => false
            },
            'safebrowsing' => {
              'enabled' => false,
              'disable_download_protection' => true
            }
          }

          # Set headless with docker friendly args.
          chrome_args = %w[window-size=1024,768 disable-gpu no-sandbox disable-translate no-default-browser-check disable-popup-blocking]
          # To run full browser instead of headless mode, run this command: HEADLESS=false rspec spec
          unless ENV.fetch('HEADLESS', 'true') == 'false'
            chrome_args += %w[headless]
          end

          # Initialize chromedriver.
          capabilities = Selenium::WebDriver::Remote::Capabilities.chrome(
            chromeOptions: {
              prefs: chrome_prefs,
              args: chrome_args
            }
          )
          driver = Capybara::Selenium::Driver.new(app, browser: :chrome, desired_capabilities: capabilities)

          driver
        end

This enables running chrome in headless mode. Headless mode just means driving chrome without rendering it on your screen.
This will greatly increase performance and memory usage keeping your CI builds snappy.

If you also want to test file downloads, add a new file in spec/support called downloads.rb with this code::

        module DownloadHelpers
          TIMEOUT = 10
          PATH    = Rails.root.join('tmp/downloads')

          extend self

          def downloads
            Dir[PATH.join('*')]
          end

          def download
            downloads.first
          end

          def download_content
            wait_for_download
            File.read(download)
          end

          def wait_for_download
            Timeout.timeout(TIMEOUT) do
              sleep 0.3 until downloaded?
            end
          end

          def downloaded?
            !downloading? && downloads.any?
          end

          def downloading?
            downloads.grep(/\.crdownload$/).any?
          end

          def clear_downloads
            FileUtils.rm_f(downloads)
          end
        end

Now add this to chrome_setup.rb::

        # Allow file downloads to work in chromedriver headless mode.
        bridge = driver.browser.send(:bridge)
        path = '/session/:session_id/chromium/send_command'
        path[':session_id'] = bridge.session_id
        bridge.http.call(:post, path, cmd: 'Page.setDownloadBehavior',
          params: {
            behavior: 'allow',
            downloadPath: DownloadHelpers::PATH.to_s
          }
        )

You're ready to write your first feature test. Here is a very basic example::

        feature 'Viewing Project', js: true do
          scenario 'project owner can view project' do
            login_as project_owner
            visit project_path
            fill_in 'Name', with: 'Test Project'
            click_on 'Create Project'
            visit projects_path

            expect(page).to have_content('Test Project')
          end
        end

Now run this command::

        HEADLESS=false rspec spec

A chrome browser will launch and be driven by your test.
