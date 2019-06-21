<template>
    <div>
        <div v-if="newKeywords.length > 0">
            <span class="font-italic" style="color: rebeccapurple;">New keywords: </span>
            <span v-for="newKeyword in newKeywords" class="badge badge-danger ml-1">
                {{ newKeyword }}
            </span>
        </div>
        <div class="btn-group m-2" role="group" aria-label="Basic example">
            <button v-bind:class="{'btn-primary': service === 'all', 'btn-secondary': service !== 'all'}"
                    @click="service = 'all'; fetchScrapedPosts();"
                    type="button" class="btn">All</button>
            <button v-bind:class="{'btn-primary': service === 'wykop', 'btn-secondary': service !== 'wykop'}"
                    @click="service = 'wykop'; fetchScrapedPosts();"
                    type="button" class="btn">Wykop</button>
            <button v-bind:class="{'btn-primary': service === 'twitter', 'btn-secondary': service !== 'twitter'}"
                    @click="service = 'twitter';  fetchScrapedPosts();"
                    type="button" class="btn">Twitter</button>
        </div>
        <div class="btn-group m-2" role="group" aria-label="Basic example">
            <button v-bind:class="{'btn-primary': owner === 'all', 'btn-secondary': owner !== 'all'}"
                    @click="owner = 'all'; fetchScrapedPosts();"
                    type="button" class="btn">All</button>
            <button v-bind:class="{'btn-primary': owner === 'yours', 'btn-secondary': owner !== 'yours'}"
                    @click="owner = 'yours'; fetchScrapedPosts();"
                    type="button" class="btn">Only yours</button>
        </div>
        <span>Filter by keyword: </span>
        <input type="text" placeholder="keyword" v-model="filterKeyword">
        <div>
            <div class="row" v-for="scrapedPost in scrapedPosts">
                <div class="col" v-if="scrapedPost.keyword.includes(filterKeyword)">
                    <div class="card m-2">
                        <div class="card-header">
                            <span @onclick="openNewWindow(scrapedPost.url)">
                                {{ scrapedPost.title }}
                            </span>
                            <span class="badge badge-info">
                                {{ scrapedPost.site }}
                            </span>
                            <span class="badge badge-warning ml-1">
                                {{ scrapedPost.keyword }}
                            </span>
                            <span style="float: right;">
                                <span class="font-italic">Posted: </span>
                                <span class="small"> {{ scrapedPost.createdDatetime }}</span>
                            </span>
                        </div>
                        <div class="card-body">
                            <div class="row">
                                <div class="col-10">
                                    <p class="card-text"> {{ scrapedPost.description }} </p>
                                </div>
                                <div class="col-2">
                                    <button @click="openNewWindow(scrapedPost.url)"
                                            type="button" class="btn btn-info">
                                        <span v-if="scrapedPost.site === 'wykop'">
                                            Go to post
                                        </span>
                                        <span v-if="scrapedPost.site === 'twitter'">
                                            Go to profile
                                        </span>
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>

import scrapedPostApi from "./scraped-post-api"
    import notificationApi from "./notification-api"
    import store from '../store'

    export default {
        name: "Visualization",
        data() {
            return {
                service: 'all',
                owner: 'all',
                scrapedPosts: [],
                colsPerRow: 2,
                filterKeyword: '',
                newKeywords: []
            }
        },
        methods: {
            fetchScrapedPosts: function () {
                this.scrapedPosts = [];
                if (this.service === 'all' && this.owner === 'all') {
                    scrapedPostApi.getScrapedPosts().then(response => {
                        this.scrapedPosts = response.data;
                    }).catch(error => {
                        console.log("Problem with server", error);
                    });
                } else if (this.service !== 'all' && this.owner === 'all') {
                    scrapedPostApi.getScrapedPostsBySite(this.service).then(response => {
                        this.scrapedPosts = response.data;
                    }).catch(error => {
                        console.log("Problem with server", error);
                    });
                } else if (this.service === 'all' && this.owner !== 'all') {
                    scrapedPostApi.getScrapedPostsByUserKeywords(store.getters.username).then(response => {
                        this.scrapedPosts = response.data;
                    }).catch(error => {
                        console.log("Problem with server", error);
                    });
                } else if (this.service !== 'all' && this.owner !== 'all') {
                    scrapedPostApi.getScrapedPostsBySiteAndUserKeywords(this.service, store.getters.username)
                        .then(response => {
                            this.scrapedPosts = response.data;
                        }).catch(error => {
                            console.log("Problem with server", error);
                        });
                }
            },
            popNotifications: function () {
                notificationApi.popNotifications(store.getters.username).then(response => {
                    this.newKeywords = response.data;
                }).catch(error => {
                    console.log("Problem with server", error);
                });
            },
            openNewWindow: function (url) {
                window.open(url, '_blank');
            }
        },
        beforeMount() {
            this.fetchScrapedPosts();
            this.popNotifications();
        }
    }
</script>

<style scoped>

</style>