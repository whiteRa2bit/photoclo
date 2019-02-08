<template>
    <div class="gallery">
        <imageItem v-for="(image, index) in images" v-on:click.native='clicked(index)' v-bind:imageURL="image.url"/>

        <div id="myModal" class="imageModal">
            <div class="image-modal-content">
                <imageWBBItem id="imageBigShow" v-bind:faces="this.faces" v-bind:image="this.images[this.index]" />
            </div>
            <span class="close" id="closeImageButton">&times;</span>
        </div>

 
    </div>
</template>

<script>
    import imageItem from './imageItem.vue';
    import imageWBBItem from './imageWBBItem.vue';
    import axios from 'axios';

    window.onload = function() {
        var modal = document.getElementById('myModal');

        var span = document.getElementById('closeImageButton'); 

        span.onclick = function() {
            this.index = null;
            modal.style.display = "none";
        }
    }

    export default {
        name: 'gallery',
        components: {
            imageItem,
            imageWBBItem
        },
        props: {
            images: {
              type: Array,
              default () {
                  return [];
              }
            },
        },
        data() {
            return {
                index: null,
                imagenowURL: '',
                faces: {},
            };
        },
        watch: {
            index(value) {
                this.imagenowURL = this.images[value];
                this.getFaces();
            },
        },
        methods: {
            clicked(index) {
                this.index = index;
                var modal = document.getElementById('myModal');
                modal.style.display = "flex";
            },
            getFaces() {
                var this_ = this;
                if (!this_.images || ! this_.index) {
                    this_.faces = {};
                    return;
                }
                axios.get('api/faces/' + String(this_.images[this_.index].id) + '/', { headers: {Authorization: "Token " + localStorage.token}}).then(function (response) {
                        console.log('faces = ', response.data.faces);
                        this_.faces = response.data.faces;
                }).catch(function (error) {
                    console.log(error);
                    this_.faces = {};
                });
            }
        }
    }
</script>

<style>
    .gallery {
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
        justify-content: space-between;
        margin: 10px;
    }

    .imageModal {
        display: none; /* Hidden by default */
        position: fixed; /* Stay in place */
        justify-content: space-around;
        align-content: center;
        align-items: center;
        align-self: center;
        z-index: 1; /* Sit on top */
        padding-top: 300px; /* Location of the box */
        left: 0;
        top: 0;
        width: 100%; /* Full width */
        height: 100%; /* Full height */
        overflow: auto; /* Enable scroll if needed */
        background-color: rgb(0,0,0); /* Fallback color */
        background-color: rgba(0,0,0,0.9); /* Black w/ opacity */
    }

    /* Modal Content (Image) */
    .image-modal-content {
        display: flex;
        margin: auto;
        justify-content: space-around;
        align-content: center;
        align-self: center;
        align-items: center;
        width: auto;
        height: auto;
        background-color: rgba(0, 0, 0, 0) !important;

    }
    
    /* Add Animation - Zoom in the Modal */
    .image-modal-content { 
        animation-name: zoom;
        animation-duration: 0.6s;
    }

    @keyframes zoom {
        from {transform:scale(0)} 
        to {transform:scale(1)}
    }

    /* The Close Button */
    .close {
        position: absolute;
        top: 15px;
        right: 35px;
        color: #FFFFFF !important;
        font-size: 40px;
        font-weight: bold;
        transition: 0.3s;
    }

    .close:hover,
    .close:focus {
        color: #bbb;
        text-decoration: none;
        cursor: pointer;
    }
</style>