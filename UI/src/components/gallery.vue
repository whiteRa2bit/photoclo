<template>
    <div class="gallery">
        <imageItem v-for="(image, index) in images" v-on:click.native='clicked(index)' v-bind:imageURL="image.url"/>

        <div id="myModal" class="modal">
            <div class="modal-content">
                <imageWBBItem id="imageBigShow" v-bind:image="this.images[this.index]" />
            </div>
            <span class="close" id="closeImageButton">&times;</span>
        </div>

 
    </div>
</template>

<script>
    import imageItem from './imageItem.vue';
    import imageWBBItem from './imageWBBItem';

    window.onload = function() { 
        var modal = document.getElementById('myModal');

        var span = document.getElementById('closeImageButton'); 

        span.onclick = function() {
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
            };
        },
        watch: {
            index(value) {
                this.imagenowURL = this.images[value];
            },
        },
        methods: {
            clicked(index) {
                this.index = index;
                console.log(index);
                var modal = document.getElementById('myModal');
                modal.style.display = "block";
            },
        }
    }
</script>

<style>
    .gallery {
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
        justify-content: space-around;
        margin: 10px;
    }

    .modal {
        display: none; /* Hidden by default */
        position: fixed; /* Stay in place */
        z-index: 1; /* Sit on top */
        padding-top: 100px; /* Location of the box */
        left: 0;
        top: 0;
        width: 100%; /* Full width */
        height: 100%; /* Full height */
        overflow: auto; /* Enable scroll if needed */
        background-color: rgb(0,0,0); /* Fallback color */
        background-color: rgba(0,0,0,0.9); /* Black w/ opacity */
    }

    /* Modal Content (Image) */
    .modal-content {
        display: flex;
        justify-content: space-around;
        align-content: center;
        width: 80%;
        height: 100%;
        background-color: rgba(1, 1, 1, 0) !important;
        color: blue;

    }
    
    /* Add Animation - Zoom in the Modal */
    .modal-content { 
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