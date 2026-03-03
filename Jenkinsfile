pipeline {
  agent any

  environment {
    // Repo + deploy directory on remote hosts
    REPO_URL = 'https://github.com/mehdiamar15/hello-cicd-python.git'
    APP_DIR  = '/config/hello-cicd-python'

    // Ensure tests run with the intended Python (workspace venv)
    PYTHON_BIN = 'python3'
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('CI: Install + Test') {
      steps {
        sh '''
          set -e
          pwd
          ls -la

          ${PYTHON_BIN} -m venv .venv
          . .venv/bin/activate
          python -V

          pip install -U pip
          pip install -r requirements.txt -r requirements-dev.txt

          # Make sure Django settings are visible to pytest-django
          export DJANGO_SETTINGS_MODULE=config.settings
          export PYTHONPATH="$PWD"

          pytest -q
        '''
      }
    }

    stage('CD: Deploy to Development') {
      steps {
        sh '''
          set -e

          ssh -o StrictHostKeyChecking=no \
              -o ServerAliveInterval=10 \
              -o ServerAliveCountMax=3 \
              -i /var/jenkins_home/.ssh/id_ed25519 \
              -p 2222 dev@development "
                set -e

                APP_DIR=\"${APP_DIR}\"
                REPO_URL=\"${REPO_URL}\"

                if [ ! -d \"$APP_DIR/.git\" ]; then
                  git clone \"$REPO_URL\" \"$APP_DIR\"
                fi

                cd \"$APP_DIR\"
                git fetch --all
                git reset --hard origin/main

                python3 -m venv .venv
                . .venv/bin/activate
                python -V

                pip install -U pip
                pip install -r requirements.txt

                python manage.py migrate --noinput

                # Stop previous gunicorn if running
                pkill -f \"gunicorn config.wsgi:application\" || true

                # Start detached (no stdin), log to file
                nohup .venv/bin/gunicorn config.wsgi:application \
                  --bind 0.0.0.0:80 \
                  </dev/null >/tmp/django_dev.log 2>&1 &

                sleep 1
                echo DEV_DEPLOYED
              "
        '''
      }
    }

    stage('CD: Deploy to Staging') {
      steps {
        sh '''
          set -e

          ssh -o StrictHostKeyChecking=no \
              -o ServerAliveInterval=10 \
              -o ServerAliveCountMax=3 \
              -i /var/jenkins_home/.ssh/id_ed25519 \
              -p 2222 mehdi@mehdi "
                set -e

                APP_DIR=\"${APP_DIR}\"
                REPO_URL=\"${REPO_URL}\"

                if [ ! -d \"$APP_DIR/.git\" ]; then
                  git clone \"$REPO_URL\" \"$APP_DIR\"
                fi

                cd \"$APP_DIR\"
                git fetch --all
                git reset --hard origin/main

                python3 -m venv .venv
                . .venv/bin/activate
                python -V

                pip install -U pip
                pip install -r requirements.txt

                python manage.py migrate --noinput

                pkill -f \"gunicorn config.wsgi:application\" || true

                nohup .venv/bin/gunicorn config.wsgi:application \
                  --bind 0.0.0.0:80 \
                  </dev/null >/tmp/django_stage.log 2>&1 &

                sleep 1
                echo STAGE_DEPLOYED
              "
        '''
      }
    }

    stage('CD: Deploy to Production (Manual)') {
      steps {
        input message: 'Deploy to PRODUCTION (adam)?', ok: 'Deploy'

        sh '''
          set -e

          ssh -o StrictHostKeyChecking=no \
              -o ServerAliveInterval=10 \
              -o ServerAliveCountMax=3 \
              -i /var/jenkins_home/.ssh/id_ed25519 \
              -p 2222 adam@adam "
                set -e

                APP_DIR=\"${APP_DIR}\"
                REPO_URL=\"${REPO_URL}\"

                if [ ! -d \"$APP_DIR/.git\" ]; then
                  git clone \"$REPO_URL\" \"$APP_DIR\"
                fi

                cd \"$APP_DIR\"
                git fetch --all
                git reset --hard origin/main

                python3 -m venv .venv
                . .venv/bin/activate
                python -V

                pip install -U pip
                pip install -r requirements.txt

                python manage.py migrate --noinput

                pkill -f \"gunicorn config.wsgi:application\" || true

                nohup .venv/bin/gunicorn config.wsgi:application \
                  --bind 0.0.0.0:80 \
                  </dev/null >/tmp/django_prod.log 2>&1 &

                sleep 1
                echo PROD_DEPLOYED
              "
        '''
      }
    }
  }
}

