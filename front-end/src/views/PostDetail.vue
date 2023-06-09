<template>
  <div class="container">
    <div v-if="loading">
      <div class="notification is-primary">Loading...</div>
    </div>
    <div v-else-if="post" class="box">
      <article class="media">
        <div class="media-content">
          <h1 class="title">{{ post.title }}</h1>
          <p class="subtitle" style="white-space: pre-wrap">{{ post.description }}</p>
          <figure class="image">
            <a :href="post.get_image" target="_blank">
              <img :src="post.get_image" :style="{
                  filter: blur ? 'blur(10px)' : 'none',
                  'max-height': '300px',
                  'max-width': '300px',
                }" alt="Post image" />
            </a>
          </figure>
          <div class="level">
            <div class="level-left">
              <p class="level-item">
                <span class="icon is-small">
                  <i class="fas fa-user"></i>
                </span>
                {{ post.author }}
              </p>
              <p class="level-item">
                <span class="icon is-small">
                  <i class="fas fa-clock"></i>
                </span>
                {{ post.time_since_post }}
              </p>
            </div>
            <div class="level-right">
              <span class="tag is-info">{{ post.category }}</span>
            </div>
          </div>
          <hr />
          <h2 class="subtitle level">
            <div class="level-left">
              Comments
            </div>
            <div class="level-right">
              <button class="button is-primary" @click="showCommentForm = !showCommentForm">{{ showCommentForm ? 'Cancel' : 'Add Comment' }}</button>
            </div>
          </h2>
          <div class="comments">
            <form class="mt-3" v-if="showCommentForm" @submit.prevent="addComment">
              <div class="field">
                <label class="label">Add Comment</label>
                <div class="control">
                  <textarea class="textarea" v-model="newCommentText" placeholder="Write your comment here"></textarea>
                </div>
              </div>
              <div class="control">
                <button type="submit" class="button is-primary">Submit</button>
              </div>
            </form>
          </div>
          <CommentBox :comments="post.comments" @add-comment="addComment" @add-reply="addReply" @delete-comment="deleteComment" @delete-reply="deleteReply"/>
        </div>
      </article>
    </div>
  </div>
</template>

<script>
import { getAPI } from "@/plugins/axios";
import CommentBox from "@/components/CommentBox.vue";

export default {
  name: "PostDetail",
  components: {
    CommentBox,
  },
  data() {
    return {
      post: undefined,
      loading: false,
      newCommentText: "",
      showCommentForm: false,
    };
  },
  computed: {
    postSlug() {
      return this.$route.params.slug;
    },
  },
  watch: {
    postSlug: {
      immediate: true,
      handler: async function () {
        await this.fetchPost();
      },
    },
  },
  methods: {
    async fetchPost() {
      const token = localStorage.getItem("access");
      const post_slug = this.postSlug;

      if (!post_slug) {
        this.$router.go();
      }

      console.log("API endpoint:", getAPI.defaults.baseURL);
      console.log("postSlug:", post_slug);

      this.loading = true;

      try {
        const response = await getAPI.get(`/api/v1/posts/${post_slug}/`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        console.log("Post API has received data");
        this.post = Object.assign({}, response.data);

        const commentsResponse = await getAPI.get(
          `/api/v1/posts/${this.post.id}/comments/`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );
        this.post.comments = commentsResponse.data;

        localStorage.setItem("post_slug", post_slug);
      } catch (error) {
        console.log(error);
        this.error = error;
        return Promise.reject(error);
      } finally {
        this.loading = false;
      }
    },

    addComment() {
      const token = localStorage.getItem("access");
      const post_slug = this.postSlug;

      getAPI
        .post(
          `/api/v1/posts/${post_slug}/comments/`,
          {
            text: this.newCommentText,
            post_slug: post_slug,
          },
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        )
        .then((response) => {
          console.log("Comment has been added");
          this.post.comments.push(response.data);
          this.newCommentText = "";
          this.fetchPost();
        })
        .catch((error) => {
          console.log(error);
        });
    },
    // ...
    addReply({ parentCommentId, text }) {
      const token = localStorage.getItem("access");
      const post_slug = this.postSlug;

      getAPI
        .post(
          `/api/v1/posts/${post_slug}/comments/`,
          {
            text: text,
            post_slug: post_slug,
            parent_comment: parentCommentId,
          },
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        )
        .then((response) => {
          const parentComment = this.post.comments.find(
            (comment) => comment.id === parentCommentId
          );
          parentComment.children.push(response.data);
        });
    },
    deleteComment(commentId) {
      const token = localStorage.getItem("access");
      const post_slug = this.postSlug;

      getAPI
        .delete(`/api/v1/posts/${post_slug}/comments/${commentId}/delete/`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        .then(() => {
          const index = this.post.comments.findIndex(comment => comment.id === commentId);
          this.post.comments.splice(index, 1);
        });
    },
    deleteReply(replyId) {
      const token = localStorage.getItem("access");
      const post_slug = this.postSlug;

      getAPI
        .delete(`/api/v1/posts/${post_slug}/comments/${replyId}/delete/`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        .then(() => {
          // Find the parent comment of the reply
          const parentComment = this.post.comments.find(comment => comment.children.some(reply => reply.id === replyId));

          // Remove the reply from the parent comment's children array
          const index = parentComment.children.findIndex(reply => reply.id === replyId);
          parentComment.children.splice(index, 1);
        });
    },
    unmounted() {
      localStorage.removeItem("post_slug");
    },
  },
};
</script>

<style scoped>
@media screen and (max-width: 768px) {
  .comments form {
    width: 100%;
  }
}
</style>
