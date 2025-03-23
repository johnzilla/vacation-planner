# CI/CD Setup Guide

This document provides guidance on setting up Continuous Integration and Continuous Deployment (CI/CD) for the Vacation Planner application.

## GitHub Actions CI Pipeline

Create a `.github/workflows/ci.yml` file in the root directory:

```yaml
name: CI Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test-backend:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        cd backend
        pip install -r requirements.txt
        pip install pytest pytest-cov

    - name: Run tests
      run: |
        cd backend
        pytest --cov=app

    - name: Upload coverage report
      uses: codecov/codecov-action@v3
      with:
        directory: ./backend
        flags: backend

  test-frontend:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'

    - name: Install dependencies
      run: |
        cd frontend/web
        npm ci

    - name: Run tests
      run: |
        cd frontend/web
        npm test

    - name: Upload coverage report
      uses: codecov/codecov-action@v3
      with:
        directory: ./frontend/web/coverage
        flags: frontend

  lint:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'

    - name: Install Python linting tools
      run: |
        python -m pip install --upgrade pip
        pip install flake8 black isort

    - name: Set up Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'

    - name: Install Node.js linting tools
      run: |
        cd frontend/web
        npm ci

    - name: Lint Python code
      run: |
        cd backend
        flake8 .
        black --check .
        isort --check .

    - name: Lint JavaScript/Svelte code
      run: |
        cd frontend/web
        npx eslint .
        npx prettier --check .

  build:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2

    - name: Build backend Docker image
      uses: docker/build-push-action@v4
      with:
        context: ./backend
        push: false
        tags: vacation-planner-backend:latest
        cache-from: type=gha
        cache-to: type=gha,mode=max

    - name: Build frontend Docker image
      uses: docker/build-push-action@v4
      with:
        context: ./frontend/web
        push: false
        tags: vacation-planner-frontend:latest
        cache-from: type=gha
        cache-to: type=gha,mode=max
```

## GitHub Actions CD Pipeline (Optional)

For automated deployment, create a `.github/workflows/cd.yml` file:

```yaml
name: CD Pipeline

on:
  push:
    branches: [ main ]
    tags: [ 'v*' ]

jobs:
  deploy-backend:
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && (github.ref == 'refs/heads/main' || startsWith(github.ref, 'refs/tags/v'))

    steps:
    - uses: actions/checkout@v3

    - name: Set up Fly.io CLI
      uses: superfly/flyctl-actions/setup-flyctl@master

    - name: Deploy to Fly.io
      run: |
        cd backend
        flyctl deploy --remote-only
      env:
        FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN }}

  deploy-frontend:
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && (github.ref == 'refs/heads/main' || startsWith(github.ref, 'refs/tags/v'))

    steps:
    - uses: actions/checkout@v3

    - name: Set up Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'

    - name: Install dependencies
      run: |
        cd frontend/web
        npm ci

    - name: Build
      run: |
        cd frontend/web
        npm run build

    - name: Deploy to Vercel
      uses: amondnet/vercel-action@v20
      with:
        vercel-token: ${{ secrets.VERCEL_TOKEN }}
        vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
        vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
        working-directory: ./frontend/web
        vercel-args: '--prod'
```

## GitLab CI/CD (Alternative)

If you're using GitLab instead of GitHub, create a `.gitlab-ci.yml` file in the root directory:

```yaml
stages:
  - test
  - lint
  - build
  - deploy

variables:
  DOCKER_DRIVER: overlay2
  DOCKER_TLS_CERTDIR: ""

test-backend:
  stage: test
  image: python:3.9-slim
  script:
    - cd backend
    - pip install -r requirements.txt
    - pip install pytest pytest-cov
    - pytest --cov=app
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: backend/coverage.xml

test-frontend:
  stage: test
  image: node:18-alpine
  script:
    - cd frontend/web
    - npm ci
    - npm test
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: frontend/web/coverage/cobertura-coverage.xml

lint-backend:
  stage: lint
  image: python:3.9-slim
  script:
    - pip install flake8 black isort
    - cd backend
    - flake8 .
    - black --check .
    - isort --check .

lint-frontend:
  stage: lint
  image: node:18-alpine
  script:
    - cd frontend/web
    - npm ci
    - npx eslint .
    - npx prettier --check .

build-backend:
  stage: build
  image: docker:20.10.16
  services:
    - docker:20.10.16-dind
  script:
    - cd backend
    - docker build -t vacation-planner-backend:latest .

build-frontend:
  stage: build
  image: docker:20.10.16
  services:
    - docker:20.10.16-dind
  script:
    - cd frontend/web
    - docker build -t vacation-planner-frontend:latest .

deploy-backend:
  stage: deploy
  image: alpine:latest
  script:
    - apk add --no-cache curl
    - curl -L https://fly.io/install.sh | sh
    - cd backend
    - ~/.fly/bin/flyctl deploy
  only:
    - main
    - tags

deploy-frontend:
  stage: deploy
  image: node:18-alpine
  script:
    - cd frontend/web
    - npm ci
    - npm run build
    - npx vercel --prod --token $VERCEL_TOKEN
  only:
    - main
    - tags
```

## CircleCI (Alternative)

If you're using CircleCI, create a `.circleci/config.yml` file in the root directory:

```yaml
version: 2.1

orbs:
  python: circleci/python@1.5
  node: circleci/node@5.0.2
  docker: circleci/docker@2.1.4

jobs:
  test-backend:
    docker:
      - image: cimg/python:3.9
    steps:
      - checkout
      - python/install-packages:
          pkg-manager: pip
          packages:
            - pytest
            - pytest-cov
          app-dir: backend
      - run:
          name: Run tests
          command: |
            cd backend
            pytest --cov=app
      - store_test_results:
          path: backend/test-results

  test-frontend:
    docker:
      - image: cimg/node:18.12
    steps:
      - checkout
      - node/install-packages:
          app-dir: frontend/web
      - run:
          name: Run tests
          command: |
            cd frontend/web
            npm test
      - store_test_results:
          path: frontend/web/test-results

  lint:
    docker:
      - image: cimg/python:3.9-node
    steps:
      - checkout
      - python/install-packages:
          pkg-manager: pip
          packages:
            - flake8
            - black
            - isort
      - node/install-packages:
          app-dir: frontend/web
      - run:
          name: Lint Python code
          command: |
            cd backend
            flake8 .
            black --check .
            isort --check .
      - run:
          name: Lint JavaScript/Svelte code
          command: |
            cd frontend/web
            npx eslint .
            npx prettier --check .

  build:
    docker:
      - image: cimg/base:2022.06
    steps:
      - checkout
      - setup_remote_docker:
          version: 20.10.14
      - run:
          name: Build backend Docker image
          command: |
            cd backend
            docker build -t vacation-planner-backend:latest .
      - run:
          name: Build frontend Docker image
          command: |
            cd frontend/web
            docker build -t vacation-planner-frontend:latest .

  deploy:
    docker:
      - image: cimg/base:2022.06
    steps:
      - checkout
      - run:
          name: Install Fly.io CLI
          command: |
            curl -L https://fly.io/install.sh | sh
      - run:
          name: Deploy backend to Fly.io
          command: |
            cd backend
            ~/.fly/bin/flyctl deploy
      - run:
          name: Install Node.js
          command: |
            curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
            sudo apt-get install -y nodejs
      - run:
          name: Deploy frontend to Vercel
          command: |
            cd frontend/web
            npm ci
            npm run build
            npx vercel --prod --token $VERCEL_TOKEN

workflows:
  version: 2
  build-test-deploy:
    jobs:
      - test-backend
      - test-frontend
      - lint
      - build:
          requires:
            - test-backend
            - test-frontend
            - lint
      - deploy:
          requires:
            - build
          filters:
            branches:
              only: main
            tags:
              only: /^v.*/
```

## Simple CI/CD for Solo Developer

For a solo developer working on an MVP, a simplified CI/CD setup might be more appropriate. Here's a minimal GitHub Actions workflow:

```yaml
name: Simple CI/CD

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build-and-test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'

    - name: Install Python dependencies
      run: |
        python -m pip install --upgrade pip
        cd backend
        pip install -r requirements.txt
        pip install pytest

    - name: Set up Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'

    - name: Install Node.js dependencies
      run: |
        cd frontend/web
        npm ci

    - name: Run backend tests
      run: |
        cd backend
        pytest

    - name: Build frontend
      run: |
        cd frontend/web
        npm run build

    - name: Deploy to Fly.io (if main branch)
      if: github.ref == 'refs/heads/main' && github.event_name == 'push'
      run: |
        curl -L https://fly.io/install.sh | sh
        cd backend
        ~/.fly/bin/flyctl deploy
      env:
        FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN }}

    - name: Deploy to Vercel (if main branch)
      if: github.ref == 'refs/heads/main' && github.event_name == 'push'
      uses: amondnet/vercel-action@v20
      with:
        vercel-token: ${{ secrets.VERCEL_TOKEN }}
        vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
        vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
        working-directory: ./frontend/web
        vercel-args: '--prod'
```

## Setting Up Secrets

For deployment, you'll need to set up secrets in your CI/CD platform:

### GitHub Actions Secrets

1. Go to your GitHub repository
2. Click on "Settings" > "Secrets and variables" > "Actions"
3. Add the following secrets:
   - `FLY_API_TOKEN`: Your Fly.io API token
   - `VERCEL_TOKEN`: Your Vercel API token
   - `VERCEL_ORG_ID`: Your Vercel organization ID
   - `VERCEL_PROJECT_ID`: Your Vercel project ID

### GitLab CI/CD Variables

1. Go to your GitLab project
2. Click on "Settings" > "CI/CD"
3. Expand the "Variables" section
4. Add the same variables as above

### CircleCI Environment Variables

1. Go to your CircleCI project
2. Click on "Project Settings" > "Environment Variables"
3. Add the same variables as above

## Best Practices for CI/CD

1. **Start Simple**: Begin with a basic CI pipeline that just runs tests and linting.

2. **Automate Incrementally**: Add more automation as your project matures.

3. **Test Before Deploy**: Always run tests before deploying to production.

4. **Use Staging Environments**: Deploy to a staging environment before production.

5. **Monitor Deployments**: Set up notifications for successful/failed deployments.

6. **Keep Secrets Secure**: Never commit secrets to your repository.

7. **Cache Dependencies**: Use caching to speed up your CI/CD pipeline.

8. **Parallel Jobs**: Run independent jobs in parallel to save time.

## Recommended CI/CD Setup for Solo Developer MVP

For a solo developer working on an MVP, I recommend:

1. **Start with GitHub Actions**: It's free for public repositories and has good integration with GitHub.

2. **Use the Simple CI/CD Workflow**: The simplified workflow above is a good starting point.

3. **Focus on Automated Testing**: Ensure your tests run on every push.

4. **Add Deployment Later**: Once your project is more stable, add automated deployment.

5. **Use Docker for Consistency**: Docker ensures your application runs the same way in CI/CD as it does locally.
