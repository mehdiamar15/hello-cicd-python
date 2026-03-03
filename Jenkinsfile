pipeline {
  agent any

  environment {
    REPO_URL = 'https://github.com/mehdiamar15/hello-cicd-python.git'
    APP_DIR  = '/config/hello-cicd-python'
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
          python3 -m venv .venv
          . .venv/bin/activate
          pip install -U pip
          pip install -r requirements.txt -r requirements-dev.txt
          pytest -q
        '''
      }
    }

    stage('CD: Deploy to Development') {
      steps {
        sh '''
          ssh -o StrictHostKeyChecking=no -i /var/jenkins_home/.ssh/id_ed25519 -p 2222 dev@development "
            set -e
            if [ ! -d ${APP_DIR}/.git ]; then
              git clone ${REPO_URL} ${APP_DIR}
            fi
            cd ${APP_DIR}
            git fetch --all
            git reset --hard origin/main

            python3 -m venv .venv
            . .venv/bin/activate
            pip install -U pip
            pip install -r requirements.txt

            python manage.py migrate --noinput

            pkill -f gunicorn || true
            nohup .venv/bin/gunicorn config.wsgi:application --bind 0.0.0.0:80 >/tmp/django_dev.log 2>&1 &
            echo DEV_DEPLOYED
          "
        '''
      }
    }

    stage('CD: Deploy to Staging') {
      steps {
        sh '''
          ssh -o StrictHostKeyChecking=no -i /var/jenkins_home/.ssh/id_ed25519 -p 2222 mehdi@mehdi "
            set -e
            if [ ! -d ${APP_DIR}/.git ]; then
              git clone ${REPO_URL} ${APP_DIR}
            fi
            cd ${APP_DIR}
            git fetch --all
            git reset --hard origin/main

            python3 -m venv .venv
            . .venv/bin/activate
            pip install -U pip
            pip install -r requirements.txt

            python manage.py migrate --noinput

            pkill -f gunicorn || true
            nohup .venv/bin/gunicorn config.wsgi:application --bind 0.0.0.0:80 >/tmp/django_stage.log 2>&1 &
            echo STAGE_DEPLOYED
          "
        '''
      }
    }

    stage('CD: Deploy to Production (Manual)') {
      steps {
        input message: 'Deploy to PRODUCTION (adam)?', ok: 'Deploy'
        sh '''
          ssh -o StrictHostKeyChecking=no -i /var/jenkins_home/.ssh/id_ed25519 -p 2222 adam@adam "
            set -e
            if [ ! -d ${APP_DIR}/.git ]; then
              git clone ${REPO_URL} ${APP_DIR}
            fi
            cd ${APP_DIR}
            git fetch --all
            git reset --hard origin/main

            python3 -m venv .venv
            . .venv/bin/activate
            pip install -U pip
            pip install -r requirements.txt

            python manage.py migrate --noinput

            pkill -f gunicorn || true
            nohup .venv/bin/gunicorn config.wsgi:application --bind 0.0.0.0:80 >/tmp/django_prod.log 2>&1 &
            echo PROD_DEPLOYED
          "
        '''
      }
    }
  }
}
