<template>
    <gallery v-bind:images="images" />
</template>

<script>

    import gallery from './gallery.vue';
    import uploader from 'vue-simple-uploader';
    import axios from 'axios';

    import imageItem from './imageItem.vue'; 

    export default {
        components: {
            gallery,
            imageItem
        },
        name: 'Secure',
        data() {
            return {
                images: [],
                index: null
            }
        },
        mounted() {
            var this_ = this;
            axios.get('/api/photos/', { headers: {Authorization: "Token " + localStorage.token}, params: {offset: 0, limit: 2000, size: "o"}}).then(function (response) {
                for (var i = 0; i < response.data.photos.length; ++i) {
                    this_.images.push(response.data.photos[i]);
                }
            }).catch(function (error) {
                console.log(error);
            })
        },
        methods: {
        }
    }
</script>

<style scoped>
    #secure {
        background-color: rgba(0, 0, 0, 0);
        padding: 20px;
        margin-top: 10px;
        display: flex;
        flex-wrap: wrap;
        justify-content: space-around;
        flex-direction: column;
    }
    .image {
        float: left;
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center center;
        border: 1px solid #ebebeb;
        margin: 5px;
    }

    .imageView {
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
        justify-content: space-around;
    }

    .uploader-example {
        width: 880px;
        padding: 15px;
        margin: 40px auto 0;
        font-size: 12px;
        box-shadow: 0 0 10px rgba(0, 0, 0, .4);
    }
    .uploader-example .uploader-btn {
        margin-right: 4px;
    }
    .uploader-example .uploader-list {
        max-height: 440px;
        overflow: auto;
        overflow-x: hidden;
        overflow-y: auto;
    }
</style>
