<template>
  <div class="search">
    <v-form @submit.prevent="searchWord" ref="form" class="mb-6">
      <v-text-field v-model="word.name" label="Word" required></v-text-field>
      <v-btn color="info" class="mr-4" type="submit">
        Search
      </v-btn>
    </v-form>
    <p v-if="notFound">No results found</p>
    <v-card elevation="2" v-if="word.variants.length" class="mb-6">
      <v-card-title>
        Results
      </v-card-title>
      <v-list-item v-for="variant in word.variants" :key="variant.id">
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
        <v-btn
          v-if="!alreadySaved"
          tile
          color="info"
          text
          v-on:click="saveWord"
        >
          <v-icon left>
            mdi-plus
          </v-icon>
          Save
        </v-btn>

        <v-btn v-if="alreadySaved" tile disabled text>
          Saved
        </v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import apiClient from "../api_client";

const blankWord = { name: null, id: null, variants: [] };

export default Vue.extend({
  name: "Search",
  data: () => ({
    word: blankWord,
    variants: [],
    notFound: false,
    alreadySaved: false
  }),
  methods: {
    searchWord: function() {
      apiClient
        .get(`/search/${this.word.name}`, {
          validateStatus: status => status === 200
        })
        .then(response => {
          this.word = response.data;
          this.notFound = false;
          this.checkAlreadySaved();
        })
        .catch(err => {
          if (err.response && err.response.status === 404) {
            this.word = blankWord;
            this.notFound = true;
          }
        });
    },
    saveWord: function() {
      apiClient.post(`/words/${this.word.id}`).then(response => {
        this.$store.state.words.push(this.word);
        this.alreadySaved = true;
      });
    },
    deleteWord: function(wordId: number) {
      apiClient.delete(`/words/${wordId}`);
    },
    checkAlreadySaved: function() {
      let i;

      for (i = 0; i < this.$store.state.words.length; i++) {
        if (this.$store.state.words[i].id === this.word.id) {
          this.alreadySaved = true;
          return;
        }
      }

      this.alreadySaved = false;
    }
  }
});
</script>
