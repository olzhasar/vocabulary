<template>
  <div class="search">
    <v-form @submit.prevent="searchWord" ref="form" class="mb-6">
      <v-text-field v-model="word" label="Word" required></v-text-field>
      <v-btn color="info" class="mr-4" type="submit">
        Search
      </v-btn>
    </v-form>
    <v-card elevation="2" v-if="variants.length">
      <v-card-title>
        Results
      </v-card-title>
      <v-list-item v-for="variant in variants" :key="variant.id">
        <v-list-item-content>
          <v-list-item-title>
            {{ variant.definition }}
          </v-list-item-title>
          <v-list-item-subtitle>
            {{ variant.part_of_speech }}
          </v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
      <v-card-actions>
        <v-btn color="info" text>Save</v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import apiClient from "../api_client";

export default Vue.extend({
  name: "Search",
  data: () => ({
    word: null,
    variants: []
  }),
  methods: {
    searchWord: function() {
      apiClient.get(`/search/${this.word}`).then(response => {
        this.variants = response.data.variants;
      });
    }
  }
});
</script>
