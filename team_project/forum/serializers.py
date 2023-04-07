from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Category, Post, PostVotes, PostComment
from rest_framework.response import Response

User = get_user_model()

class PostSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all()
    )

    class Meta:
        model = Post
        fields = [
            "id",
            "created",
            "modified",
            'time_since_post',
            "title",
            "link",
            "description",
            "description_br",
            "owner",
            'score',
            "username",
            "owner_url",
            "category",
            "category_name",
            'slug',
            'category_slug',
            'full_url',
            'user_vote',
        ]
        extra_kwargs = {
            "url": {"view_name": "api:posts", "lookup_field": "title"}
        }
        # extra_kwargs = {
        #     "url": {"view_name": "api:user-detail", "lookup_field": "username"}
        # }


class PostVotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostVotes
        fields = ['post_id', 'user_id', 'vote', 'id']

    def validate(self, data): 
        post_id = data.get('post_id')
        user_id = data.get('user_id')
        vote = data.get('vote')

        # Check if the user has already voted for the post
        if PostVotes.objects.filter(post_id=post_id, user_id=user_id).exists():
            # If the user has already voted, allow them to change their vote
            post_vote = PostVotes.objects.get(post_id=post_id, user_id=user_id)
            if vote == post_vote.vote:
                return data

        # Check if the vote is valid
        if vote not in [choice[0] for choice in PostVotes.VOTE_CHOICES]:
            raise serializers.ValidationError('Invalid vote')

        return data


class AllPostsSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all()
    )
    queryset = Post.objects.all()

    class Meta:
        model = Post
        fields = [
            "id",
            "created",
            "modified",
            'time_since_post',
            "title",
            "link",
            "description",
            "description_br",
            "owner",
            "username",
            "owner_url",
            "category",
            "category_name",
            'slug',
            'category_slug',
            'score',
            'full_url',
            'user_vote',
            'user_up_style',
            'user_down_style',
            'weighted_score',
            'age_in_days',
            'number_of_comments',
        ]
        extra_kwargs = {
            "url": {"view_name": "api:allposts", "lookup_field": "title"}
        }
        # extra_kwargs = {
        #     "url": {"view_name": "api:user-detail", "lookup_field": "username"}
        # }


class CommentSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField(
        read_only=True, method_name="get_children")

    post_id = serializers.PrimaryKeyRelatedField(
        queryset=Post.objects.all()
    )
    user_id = serializers.HiddenField(default=serializers.CurrentUserDefault())

    parent = serializers.PrimaryKeyRelatedField(
        queryset=PostComment.objects.all(), allow_null=True)

    class Meta:
        model = PostComment
        fields = [
            "id",
            "post_id",
            "created",
            "modified",
            'time_since_comment',
            "comment",
            "comment_br",
            "user_id",
            "username",
            "owner_url",
            'score',
            'user_vote',
            'user_up_style',
            'user_down_style',
            'level',
            'parent',
            'children',
            'tldr',
        ]

        extra_kwargs = {
            "url": {"view_name": "api:allposts", "lookup_field": "title"}
        }

    def get_children(self, obj):
        """ self referral field """
        serializer = CommentSerializer(
            instance=obj.comment_reply.all(),
            many=True
        )
        return serializer.data
    