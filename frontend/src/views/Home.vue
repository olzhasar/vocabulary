<template>
  <div class="home">
    <v-container fluid fill-height>
      <v-layout align-center justify-center>
        <v-flex xs12 sm8 md6>
          <div class="text-h5 text-center mb-6">My vocabulary</div>
          <search></search>
        </v-flex>
      </v-layout>
    </v-container>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import search from "../components/Search.vue";

export default Vue.extend({
  data() {
    return {
      words: [],
      searched: {
        name: null,
        data: {}
      }
    };
  },
  components: {
    search
  },
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
