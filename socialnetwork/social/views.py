from queue import PriorityQueue
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views import View
from .models import Post, UserProfile, ThreadModel, MessageModel, Notification, Image, Tag
from .forms import PostForm, ThreadForm, MessageForm, ExploreForm
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.db.models import Q
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib import messages 
import folium 
import geocoder
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="socialnetwork")

class PostListView(LoginRequiredMixin, View): 
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all().order_by('-created_on')
        form = PostForm()
        context = {
            'post_list' : posts,
            'form' : form,
        }

        return render(request, 'social/post_list.html', context)

    def post(self, request, *args, **kwargs):
        posts = Post.objects.all().order_by('-created_on')
        form = PostForm(request.POST, request.FILES)
        files = request.FILES.getlist('image')
        
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()

            for f in files: 
                img = Image(image=f)
                img.save()
                new_post.image.add(img)
            
            new_post.save()

            new_post.create_tags()
        
        context = {
            'post_list' : posts,
            'form' : form,
        }

        return render(request, 'social/post_list.html', context)

    
class PostDetailView(LoginRequiredMixin, View): 
    def get(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        user = UserProfile.objects.get(pk=post.author)
        address = post.address
        print(address)
        location = geolocator.geocode(address)
        
        if(location == None): 
            print('helo')
            context = {
            'post' : post,
             }
        else: 
            
            print(location)
            lat = location.latitude
            lng = location.longitude

            m = folium.Map(location=[lat, lng], zoom_start=12)
            folium.Marker([lat, lng]).add_to(m)
            map = m._repr_html_()

            context = {
                'post' : post,
                'map' : map,
            }
      
            
            
       
       # notification = Notification.objects.create(notification_type=2, from_user=request.user, to_user=post.author, post=post)

        return render(request, 'social/post_detail.html', context)
    

class PostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView): 
    model = Post
    fields = ['body']
    template_name = 'social/post_edit.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('post-detail', kwargs={'pk': pk})


    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    model = Post
    template_name = 'social/post_delete.html'
    success_url = reverse_lazy('post-list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class ProfileView(View): 
    def get(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)

        user = profile.user
        posts = Post.objects.filter(author=user).order_by("-created_on") 


        context = {
            'user' : user,
            'profile' : profile, 
            'posts' : posts,
            
        }

        return render(request, 'social/profile.html', context)


class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = UserProfile
    fields = ['name', 'bio', 'birth_date', 'location', 'picture']
    template_name = 'social/profile_edit.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('profile', kwargs={'pk': pk})
    
    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user
    

class Search(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('q')
        print(query)
        post_list = Post.objects.filter(
            Q(body__icontains=query) | Q(address__icontains=query)
        )
        
        context = {
            'post_list': post_list,
        }
        return render(request, 'social/search.html', context)

class ListThreads(View): 
    def get(self, request, *args, **kwargs):
        threads = ThreadModel.objects.filter(Q(user=request.user) | Q(receiver=request.user))
        form = ThreadForm()

        context = {
            'threads': threads,
            'form': form,
        }
        return render(request, 'social/inbox.html', context) 

class CreateThread(View): 
    def get(self, request, *args, **kwargs):
        form = ThreadForm()
        context = {
            'form': form
        }
        return render(request, 'social/create_thread.html', context)
    def post(self, request, *args, **kwargs):
        form = ThreadForm(request.POST)
        username = request.POST.get('username')

        try: 
            receiver = User.objects.get(username=username)
            if ThreadModel.objects.filter(user=request.user, receiver=receiver).exists():
                thread = ThreadModel.objects.filter(user=request.user, receiver=receiver)[0]
                return redirect('thread', pk=thread.pk)
            elif ThreadModel.objects.filter(user=receiver, receiver=receiver).exists():
                thread = ThreadModel.objets.filter(user=receiver, receiver=request.user)[0]
                return redirect('thread', pk=thread.pk)
            if form.is_valid(): 
                thread= ThreadModel(
                    user=request.user,
                    receiver=receiver
                )
                thread.save()
                return redirect('thread', pk=thread.pk)
        except: 
            messages.error(request, 'invalid username')
            return redirect('create-thread')

# class WriteUser(View): 
#     def post(self, request, *args, **kwargs):
#          = request.POST.get('receiver_id')
#         # request.POST.get('receiver_id', '')
#         file = request.FILES.get('file', '')
#         MessageModel.objects.create(sender_user=request.user, receiver_user=receiver_id, image=file)
#         return render(request, 'thread', {})

        

class ThreadView(View): 
    def get(self, request, pk, *args, **kwargs): 
        form = MessageForm()
        thread = ThreadModel.objects.get(pk=pk)
        message_list = MessageModel.objects.filter(thread__pk__contains=pk)
        context = {
            'thread': thread,
            'form': form,
            'message_list': message_list
        }

        return render(request, 'social/thread.html', context)
            
class CreateMessage(View):
    def post(self, request, pk, *args, **kwargs):
        form = MessageForm(request.POST, request.FILES)
        thread = ThreadModel.objects.get(pk=pk)
        if thread.receiver == request.user:
            receiver = thread.user
        else:
            receiver = thread.receiver

        if form.is_valid():
            message = form.save(commit=False)
            message.thread = thread
            message.sender_user = request.user
            message.receiver_user = receiver
            message.save()

        notification = Notification.objects.create(
            notification_type=4,
            from_user=request.user,
            to_user=receiver,
            thread=thread
        )
        return redirect('thread', pk=pk)


class PostNotification(View):
    def get(self, request, notification_pk, post_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        post = Post.objects.get(pk=post_pk)

        notification.user_has_seen = True
        notification.save()
        return redirect('post-detail', pk=post_pk)


class RemoveNotification(View): 
    def delete(self, request, notification_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)

        notification.user_has_seen = True 
        notification.save()

        return HttpResponse('success', content_type='text/plain')

class ThreadNotification(View): 
    def get(self, request, notification_pk, object_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        thread = ThreadModel.objects.get(pk=object_pk)

        notification.user_has_seen = True
        notification.save()
        return redirect('thread', pk=object_pk)

# class ExplorePage(View): 
#     def get(self, request, *args, **kwargs):
#         explore_form = ExploreForm()
#         query = self.request.GET.get('query')
#         postsearch = Post.objects.filter(name=query).first()

#         if postsearch: 
#             posts = Post.objects.filter(postsearch__in=[])
#         else: 
#             posts = Post.objects.all()
        
#         context = {
#             'tag':tag,
#             'posts':posts,
#             'explore_form': explore_form,
#         }
#         return render(request, 'social/explore.html', context)
   
    def post(self, request, *args, **kwargs):
        explore_form = ExploreForm(request.POST)
        if explore_form.is_valid():
            query = explore_form.cleaned_data['query']
            tag = Tag.objects.filter(name=query).first()

            posts = None 
            if tag: 
                posts = Post.objects.filter(tags__in=[tag])
            if posts: 
                context = {
                    'tag': tag,
                    'posts': posts,
                }
            else: 
                context = {
                    'tag' : tag,
                }
            return HttpResponseRedirect(f'/social/explore?query={query}')
        return HttpResponseRedirect('/social/explore')

""" class AdressView(View):
        address = Address.objects.all().last()
        location = geocoder.osm('LA')
        lat = location.lat
        lng = location.lng
        
        m = folium.Map(location=[4.35, 50.85], zoom_start=8)
        folium.Marker([lat, lng]).add_to(m)
        m = m._repr_html_()
        context = {
            'm' : m,
        }
 """