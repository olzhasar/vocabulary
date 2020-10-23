<template>
  <div class="home"></div>
</template>

<script lang="ts">
import Vue from "vue";

export default Vue.extend({
  methods: {
    loadWords: function() {
      this.$store.dispatch("getWords");
    }
  },
  mounted() {
    this.loadWords();
  }
});
</script>
