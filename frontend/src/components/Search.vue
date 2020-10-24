<template>
  <div class="search">
    <v-form @submit.prevent="searchWord" ref="form" class="mb-6">
      <v-text-field v-model="word.name" label="Word" required></v-text-field>
      <v-btn color="info" class="mr-4" type="submit">
        Search
      </v-btn>
    </v-form>
    <p v-if="notFound">No results found</p>
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
        <v-btn tile color="info" text v-on:click="saveWord">
          <v-icon left>
            mdi-plus
          </v-icon>
          Save
        </v-btn>
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
    word: { name: null, id: null },
    variants: [],
    notFound: false
  }),
  methods: {
    searchWord: function() {
      apiClient
        .get(`/search/${this.word.name}`, {
          validateStatus: status => status === 200
        })
        .then(response => {
          this.variants = response.data.variants;
          this.word.id = response.data.id;
          this.notFound = false;
        })
        .catch(err => {
          console.error(err);
          console.error(err.response.data);
          console.error(err.response.status);
          console.error(err.response.headers);

          if (err.response && err.response.status === 404) {
            this.variants = [];
            this.word.id = null;
            this.notFound = true;
          }
        });
    },
    saveWord: function() {
      apiClient.post(`/words/${this.word.id}`);
    },
    deleteWord: function(wordId: number) {
      apiClient.delete(`/words/${wordId}`);
    }
  }
});
</script>
