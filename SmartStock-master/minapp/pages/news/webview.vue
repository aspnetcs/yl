<template>
  <web-view :src="articleUrl"></web-view>
</template>

<script>
export default {
  data() {
    return {
      articleUrl: ''
    };
  },
  onLoad(options) {
    this.articleUrl = decodeURIComponent(options.url);
  }
};
</script>

<style scoped>
web-view {
  width: 100%;
  height: 100vh;
}
</style>