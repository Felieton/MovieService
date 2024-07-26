<template>
  <div>
    <ReviewsList type="episode" naming="name"></ReviewsList>
  </div>
</template>

<script>
import ReviewsList from "../../../components/ReviewsList";
export default {
  name: "EpisodeReviews",
  components: {ReviewsList}
}
</script>
