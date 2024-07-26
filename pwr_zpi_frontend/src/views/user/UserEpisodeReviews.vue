<template>
  <div>
    <ReviewsListUser type="episode" naming="name"></ReviewsListUser>
  </div>
</template>

<script>
import ReviewsListUser from "../../components/ReviewsListUser";
export default {
  name: "UserEpisodeReviews",
  components: {ReviewsListUser},
}
</script>