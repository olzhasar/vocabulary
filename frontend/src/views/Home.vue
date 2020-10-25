<template>
  <div class="home">
    <v-app-bar flat dense color="dark" dark>
      <v-toolbar-title>Vocabulary</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn v-on:click="logout">Logout</v-btn>
    </v-app-bar>
    <v-container fluid fill-height>
      <v-layout align-center justify-center>
        <v-flex xs12 sm8 md6>
          <search></search>

          <div v-if="this.$store.state.words.length">
            <div class="text-h6 text-center mb-3">Saved words</div>

            <v-expansion-panels v-if="this.$store.state.words.length">
              <v-expansion-panel
                v-for="word in this.$store.state.words"
                :key="word.id"
              >
                <v-expansion-panel-header>
                  {{ word.name }}
                </v-expansion-panel-header>
                <v-expansion-panel-content>
                  <v-list-item
                    v-for="variant in word.variants"
                    :key="variant.id"
                  >
                    <v-list-item-content>
                      <v-list-item-title>
                        {{ variant.definition }}
                      </v-list-item-title>
                      <v-list-item-subtitle>
                        {{ variant.part_of_speech }}
                      </v-list-item-subtitle>
                    </v-list-item-content>
                  </v-list-item>
                </v-expansion-panel-content>
              </v-expansion-panel>
            </v-expansion-panels>
          </div>
        </v-flex>
      </v-layout>
    </v-container>
    <v-card elevation="0" height="150">
      <v-footer absolute class="font-weight-medium" color="dark" dark>
        <v-col class="text-center" cols="12">
          Created by <a href="https://github.com/olzhasar/">Olzhas Arystanov</a>
        </v-col>
      </v-footer>
    </v-card>
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
    },
    logout: function() {
      this.$store.commit("removeToken");
      this.$router.push("/login");
    }
  },
  mounted() {
    this.loadWords();
  }
});
</script>
