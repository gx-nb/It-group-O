import os
from pathlib import Path

# 基础路径（不用改）
BASE_DIR = Path(__file__).resolve().parent.parent

# 密钥（开发环境不用改，部署时再换）
SECRET_KEY = 'django-insecure-abc1234567890'

# 调试模式（开发时开，部署时关）
DEBUG = True

# 允许访问的域名（部署时加PythonAnywhere的域名）
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'it-group-o-qcnu.onrender.com'
]

# 注册应用（新增accommodation、crispy_forms）
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 自定义应用
    'accommodation',
    # 表单美化（辅助前端）
    'crispy_forms',
    'crispy_bootstrap4',
]

# 中间件（不用改）
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'educheck.urls'

# 模板配置（支持前端页面）
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # 新增模板文件夹
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'educheck.wsgi.application'

# 数据库（默认SQLite，不用改，作业够用）
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 密码验证（不用改）
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# 静态文件（前端CSS/JS/图片）
STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 认证配置（登录页、权限）
LOGIN_URL = 'login'  # 未登录时跳转到登录页
LOGIN_REDIRECT_URL = 'dashboard'  # 登录后跳转到仪表盘
LOGOUT_REDIRECT_URL = 'login'  # 登出后跳转到登录页

# 表单美化配置
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
CRISPY_TEMPLATE_PACK = "bootstrap4"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"