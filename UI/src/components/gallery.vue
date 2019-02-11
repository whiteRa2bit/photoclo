<template>
    <div class="gallery">
        <imageItem v-for="(image, index) in images" v-on:click.native='clicked(index)' v-bind:imageURL="image.url" v-bind:style="styles[index]"/>

        <div id="myModal" class="imageModal">
            <span class="closeCarousel" id="closeImageButton">&times;</span>
            <div class='innerContent'>
                <div class="carouselButton" v-on:click="prev()">
                    <span >&#8249;</span>
                </div>
                <div id="overIBS">
                    <div class="image-modal-content">
                        <imageWBBItem id="imageBigShow" v-bind:faces="this.faces" v-bind:image="this.images[this.index]" v-bind:avatars="this.avatarsById"/>
                    </div>
                </div>
                <div class="carouselButton" v-on:click="next()">
                    <span>&#8250;</span>
                </div>
            </div>
        </div>

 
    </div>
</template>

<script>
    import imageItem from './imageItem.vue';
    import imageWBBItem from './imageWBBItem.vue';
    import axios from 'axios';

    export default {
        name: 'gallery',
        components: {
            imageItem,
            imageWBBItem,
        },
        props: {
            images: {
              type: Array,
              default () {
                  return [];
              }
            },
            avatars: {
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
                faces: [],
                recompute: 0,
                lastTime: 0,
            };
        },
        watch: {
            index(value) {
                this.imagenowURL = this.images[value];
                this.getFaces();
            },
        },
        created: function () {
            document.onkeydown = this.onkeydown;
            window.addEventListener('resize', this.updateStyles);
            this.updateStyles();
        },
        destroyed() {
            window.removeEventListener('resize', this.updateStyles);
        },
        computed: {
            avatarsById: function() {
                var avatarsById = {};
                for (var i = 0; i < this.avatars.length; ++i) {
                    avatarsById[this.avatars[i].id] = this.avatars[i];
                }
                return avatarsById;
            },
            styles: function() {
                this.recompute;
                var st = [];
                var w = window.innerWidth - 10;
                for (var i = 0; i < this.images.length; ++i) {
                    var j = i;
                    var sum = 0;
                    while (j < this.images.length && (j == i || sum + Math.ceil(this.images[j].width * 200 / this.images[j].height) + 10 <= w)) {
                        sum += Math.ceil(this.images[j].width * 200 / this.images[j].height) + 10;
                        ++j;
                    }
                    var h1 = Math.floor(195 * (w - (j - i) * 10) / (sum - (j - i) * 10));
                    if (j == this.images.length) {
                        if (h1 < 250) {
                            for (var k = i; k < j; ++k) {
                                st.push('height: ' + h1 + 'px !important;');
                            }
                        }
                        else {
                            for (var k = i; k < j - 1; ++k) {
                                st.push('height: ' + 200 + 'px !important;');
                            }
                            st.push('height: 200px !important; margin-right: auto !important; margin-left: 5px;');
                        }
                    }
                    else {
                        var sum2 = sum;
                        sum2 += Math.ceil(this.images[j].width * 200 / this.images[j].height) + 10;
                        var h2 = Math.floor(195 * (w - (j - i + 1) * 10) / (sum2 - (j - i + 1) * 10));
                        if (Math.abs(h2 / 200 - 1) < Math.abs(h1 / 200 - 1)) {
                            for (var k = i; k <= j; ++k) {
                                st.push('height: ' + h2 + 'px !important;');
                            }
                            ++j;
                        }
                        else {
                            for (var k = i; k < j; ++k) {
                                st.push('height: ' + h1 + 'px !important;');
                            }
                        }
                    }
                    i = j - 1;
                }
                return st;
            }
        },
        mounted: function () {
            var modal = document.getElementById('myModal');

            var span = document.getElementById('closeImageButton'); 
            span.onclick = function() {
                console.log("darova");
                this.index = null;
                modal.style.display = "none";
            }
        },
        methods: {
            clicked(index) {
                this.index = index;
                var modal = document.getElementById('myModal');
                modal.style.display = "flex";
            },
            updateStyles() {
                this.recompute += 1;
                this.lastTime = (new Date()).getTime();
            },
            getFaces() {
                var this_ = this;
                if (!this_.images || !this_.index && this.index != 0) {
                    this_.faces = {};
                    return;
                }
                axios.get('http://photoclo.ru:8000/api/faces/' + String(this_.images[this_.index].id) + '/', { headers: {Authorization: "Token " + localStorage.token}}).then(function (response) {
                        this_.faces = response.data.faces;
                }).catch(function (error) {
                    this_.faces = {};
                });
            },
            deleteLastFaces() {
                var arr = document.getElementsByClassName('mybbButton');
                for (var i = 0; i < arr.length; ++i) {
                    arr[i].style.display = "none";
                }
            },
            next() {
                this.deleteLastFaces()
                this.index += 1;
                if (this.index == this.images.length) {
                    this.index = 0;
                }
            },
            prev() {
                this.deleteLastFaces()
                this.index -= 1;
                if (this.index < 0) {
                    this.index = this.images.length - 1;
                }
            },
            close() {
                this.deleteLastFaces()
                this.index = null;
                document.getElementById('myModal').style.display = "none";
            },
            onkeydown(e) {
                if (e.key == "Escape") {
                    this.close();
                }
                else if (e.key == "ArrowRight") {
                   this.next();
                }
                else if (e.key == "ArrowLeft"){
                    this.prev();
                }
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
        margin: 5px;
    }

    .imageModal {
        display: none; /* Hidden by default */
        position: fixed; /* Stay in place */
        z-index: 1; /* Sit on top */
        padding-top: 0px; /* Location of the box */
        left: 0;
        top: 0;
        justify-content: space-around;
        width: 100%; /* Full width */
        height: 100%; /* Full height */
        overflow: auto; /* Enable scroll if needed */
        background-color: rgb(0,0,0); /* Fallback color */
        background-color: rgba(0,0,0,0.9); /* Black w/ opacity */
    }

    /* Modal Content (Image) */
    .image-modal-content {
        display: flex;
        justify-content: space-around;
        alignment-baseline: central;
        width: 100%;
        height: auto;
        max-height: 
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

    .close {
        outline: none !important;
        border: 0px !important;
    }

    /* The Close Button */
    .closeCarousel {
        position: absolute;
        top: 10px;
        right: 20px;
        color: #999 !important; 
        font-size: 30px;
        transition: 0.3s;
    }

    .closeCarousel:hover,
    .closeCarousel:focus {
        color: #FFF !important;
        text-decoration: none;
        cursor: pointer;
    }

    .carouselButton {
        display: flex;
        flex-direction: column;
        justify-content: space-around;
        text-align: center;
        width: 5%;
        font: 40px;
        color: #CCC !important;
        background-color: rgba(0, 0, 0, 0) !important;
        height: 100% !important;
        font-weight: bold;
        transition: 0.3s;
    }

    .carouselButton:hover,
    .carouselButton:focus {
        color: #FFF;
        text-decoration: none;
        cursor: pointer;
    }

    .innerContent {
        width: 100%;
        height: 100%;
        display: flex;
        justify-content: space-between;
        alignment-baseline: central;
    }

    #overIBS {
        display: flex;
        flex-direction: column;
        justify-content: space-around;
        width: 100%;
        height: 100%;
        max-height: 100vh;
    }
</style>