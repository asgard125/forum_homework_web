from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseForbidden
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from .models import *
from django.core.exceptions import PermissionDenied
from ml_forum.forms import RegisterUserForm, LoginUserForm, AddTopicForm, EditProfileForm, VerifyProfileForm, PostForm
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import random
import ml_forum.smtp_data
from django.db.models import F


class ShowSections(ListView):
    model = Section
    template_name = 'ml_forum/index.html'
    context_object_name = 'sections'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return Section.objects.filter(is_published=True)


class ShowProfile(DetailView):
    model = UserProfile
    template_name = 'ml_forum/profile.html'
    context_object_name = 'profile'
    slug_url_kwarg = 'username'


class EditProfile(UpdateView, LoginRequiredMixin):
    model = UserProfile
    form_class = EditProfileForm
    template_name = 'ml_forum/profile_edit.html'
    context_object_name = 'form'
    extra_context = {'title': 'Редактирование профиля'}
    login_url = '/login/'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_object(self, queryset=None):
        return self.request.user.userprofile

    def get_success_url(self):
        return reverse_lazy("profile",  kwargs={'username': self.request.user.username})

@login_required
def verify_profile(request, username):
    if not request.user.username == username or request.user.userprofile.verified:
        raise PermissionDenied
    if request.method == 'POST':
        form = VerifyProfileForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if data['code'] == request.user.userprofile.verify_code \
                    and request.user.userprofile.verify_code != -1:
                UserProfile.objects.filter(user=request.user).update(verified=True, verify_code=-1)
                return redirect('profile', username)
            else:
                form.add_error(None, 'Неверный код.')
    else:
        form = VerifyProfileForm()
        server = smtplib.SMTP('smtp.gmail.com: 587')
        server.starttls()
        msg = MIMEMultipart()
        msg['From'] = ml_forum.smtp_data.login
        password = ml_forum.smtp_data.password
        server.login(msg['From'], password)
        code = random.randint(100000, 999999)
        message = f"Ваш код верификации аккаунта: {code}"
        msg.attach(MIMEText(message, 'plain'))
        msg['TO'] = request.user.email
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()
        UserProfile.objects.filter(user=request.user).update(verify_code=code)
    context = {
        'form': form,
        'title': 'Подтверждение профиля'
    }
    return render(request, 'ml_forum/profile_verify.html', context=context)


class ShowTopics(ListView):
    model = Topic
    template_name = 'ml_forum/topics.html'
    context_object_name = 'topics'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.request.user.username)
        try:
            context['section'] = Section.objects.get(pk=self.kwargs['section_id'])
            if not context['section'].is_published:
                raise PermissionDenied
        except Section.DoesNotExist:
            raise Http404()
        return context

    def get_queryset(self):
        return Topic.objects.filter(is_published=True, section__pk=self.kwargs['section_id'])


@login_required
def add_topic(request, section_id):
    if not request.user.userprofile.verified:
        raise PermissionDenied
    if request.method == 'POST':
        form = AddTopicForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            topic_data = {
                'name': data['name'],
                'description': data['description'],
                'section': Section.objects.get(pk=section_id),
                'user': request.user
            }
            new_topic = Topic(**topic_data)
            new_topic.save()
            start_post_data = {
                'post': data['post'],
                'start_post': True,
                'topic': new_topic,
                'user': request.user,
                'reply_to': ' '
            }
            Post.objects.create(**start_post_data)
            Section.objects.filter(pk=section_id).update(topics_count=F("topics_count") + 1)
            return redirect('section', section_id)
    else:
        form = AddTopicForm()
    context = {
        'section_id': section_id,
        'form': form,
        'title': 'Создание темы'
    }
    return render(request, 'ml_forum/topic_create.html', context=context)


class ShowTopicPosts(ListView):
    model = Post
    template_name = 'ml_forum/topic_posts.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['section'] = Section.objects.get(pk=self.kwargs['section_id'])
            context['topic'] = Topic.objects.get(pk=self.kwargs['topic_id'])
            context['topic_id'] = self.kwargs['topic_id']
            context['section_id'] = self.kwargs['section_id']
            if not context['section'].is_published or not context['topic'].is_published:
                raise PermissionDenied
        except (Section.DoesNotExist, Topic.DoesNotExist):
            raise Http404()
        return context

    def get_queryset(self):
        return Post.objects.filter(is_published=True, topic__pk=self.kwargs['topic_id'])


class AddPost(CreateView, LoginRequiredMixin):
    model = Post
    form_class = PostForm
    template_name = 'ml_forum/post_create.html'
    context_object_name = 'form'
    extra_context = {'title': 'Добавление поста'}
    login_url = '/login/'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['section'] = Section.objects.get(pk=self.kwargs['section_id'])
            context['topic'] = Topic.objects.get(pk=self.kwargs['topic_id'])
            context['topic_id'] = self.kwargs['topic_id']
            context['section_id'] = self.kwargs['section_id']
            context['reply_to'] = self.kwargs['reply_to']
            if not context['section'].is_published or not context['topic'].is_published or not context['topic'].opened:
                raise PermissionDenied
        except (Section.DoesNotExist, Topic.DoesNotExist):
            raise Http404()
        return context

    def get_success_url(self):
        return reverse_lazy("topic", kwargs={'section_id': self.kwargs['section_id'], 'topic_id': self.kwargs['topic_id']})

    def form_valid(self, form):
        self.post = form.save(commit=False)
        self.post.user = self.request.user
        self.post.topic = Topic.objects.get(pk=self.kwargs['topic_id'])
        self.post.reply_to = self.kwargs['reply_to']
        Topic.objects.filter(pk=self.kwargs['topic_id']).update(posts_count=F("posts_count") + 1)
        UserProfile.objects.filter(user=self.request.user).update(messages_count=F("messages_count") + 1)
        self.post.save()
        return super(AddPost, self).form_valid(form)


class EditPost(UpdateView, LoginRequiredMixin):
    model = Post
    form_class = PostForm
    template_name = 'ml_forum/post_edit.html'
    context_object_name = 'form'
    extra_context = {'title': 'Редактирование поста'}
    login_url = '/login/'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            post = self.get_object()
            context['section'] = Section.objects.get(pk=self.kwargs['section_id'])
            context['topic'] = Topic.objects.get(pk=self.kwargs['topic_id'])
            context['section_id'] = self.kwargs['section_id']
            context['topic_id'] = self.kwargs['topic_id']
            context['post_id'] = self.kwargs['post_id']
            if not context['section'].is_published or not context['topic'].is_published or not context['topic'].opened \
                    or not post.user == self.request.user:
                raise PermissionDenied
        except (Section.DoesNotExist, Topic.DoesNotExist):
            raise Http404()
        return context

    def get_object(self, queryset=None):
        try:
            return Post.objects.get(pk=self.kwargs['post_id'])
        except Post.DoesNotExist:
            raise Http404()

    def get_success_url(self):
        return reverse_lazy("topic", kwargs={'section_id': self.kwargs['section_id'], 'topic_id': self.kwargs['topic_id']})


def pageNotFound(request, exception):
    return render(request, 'ml_forum/404error.html')


def pageForbidden(request, exception):
    return render(request, 'ml_forum/403error.html')


class DataMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        return context


class RegisterUser(CreateView, DataMixin):
    form_class = RegisterUserForm
    template_name = 'ml_forum/register.html'
    success_url = reverse_lazy('index')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return {**context, **c_def}

    def form_valid(self, form):
        user = form.save()
        UserProfile.objects.create(user=user, slug=user.username)
        login(self.request, user)
        return redirect('/')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'ml_forum/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Вход")
        return {**context, **c_def}

    def get_success_url(self):
        return reverse_lazy('index')


def logout_user(request):
    logout(request)
    return redirect('login')