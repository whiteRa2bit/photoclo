<template>
    <div>
        <!--<span> {{images.length}} </span>-->
        <div class="gallery">
            <imageItem v-for="(image, index) in images" v-on:click.native='clicked(index)' v-bind:key="image.id" v-bind:imageURL="image.url" v-bind:style="styles[index]"/>

            <div id="myModal" class="imageModal">
                <span class="buttonCarousel" id="closeImageButton">&times;</span>
                <div class="bottomButtons">
                    <span id="deleteImageButton">Удалить</span>
                    <span id="downloadImageButton">Загрузить</span>
                </div>
                <div class='innerContent'>
                    <div class="carouselButton" id="prevButton" v-on:click="prev()">
                        <span >&#8249;</span>
                    </div>
                    <div id="overIBS">
                        <div class="image-modal-content">
                            <imageWBBItem id="imageBigShow" v-bind:faces="this.faces" v-bind:image="imagesBig[index]" v-bind:avatars="this.avatarsById"/>
                        </div>
                    </div>
                    <div class="carouselButton" id="nextButton" v-on:click="next()">
                        <span>&#8250;</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import imageItem from './imageItem.vue';
    import imageWBBItem from './imageWBBItem.vue';
    import axios from 'axios';

    var download = function (filename) {
        var a = document.createElement("a");
        a.href = '';
        a.setAttribute("download", filename);
        var b = document.createEvent("MouseEvents");
        b.initEvent("click", false, true);
        a.dispatchEvent(b);
        return false;
    }

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
            imagesBig: {
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
                console.log("lel");
                this.imagenowURL = '';
                console.log("kek");
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
            },
        },
        mounted: function () {
            var modal = document.getElementById('myModal');

            var span = document.getElementById('closeImageButton');
            span.onclick = function () {
                this.index = null;
                modal.style.display = "none";
            }

            var span2 = document.getElementById('deleteImageButton');
            var span3 = document.getElementById('downloadImageButton');
            var this_ = this;
            span2.onclick = function () {
                if (this_.index == null) {
                    return;
                }
                var id_ = this_.images[this_.index].id;
                this_.images.splice(this_.index, 1);
                this_.imagesBig.splice(this_.index, 1);
                if (this_.index == this_.images.length) {
                    this_.index = 0;
                }
                this_.deleteLastFaces();
                if (this_.images.length == 0) {
                    this_.close();
                }
                // localStorage.imgNum = this.images.length;
                axios.delete('http://photoclo.ru:8000/api/photos/' + id_ + '/', { headers: {Authorization: "Token " + localStorage.token}}).then(function (response) {
                    console.log("deleted");
                }).catch(function (error) {
                    console.log(error);
                });
            };

            span3.onclick = function () {
                axios.get('http://photoclo.ru:8000/api/photos/' + this_.images[this_.index].id + '/download/', { headers: {Authorization: "Token " + localStorage.token}}).then(function (response) {
                    var url = response.data.url;
                    download('http://photoclo.ru:8000' + url);
                }).catch(function (error) {
                    console.log(error);
                });
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
                this.deleteLastFaces();
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
        display: none;
        position: fixed;
        z-index: 1;
        padding-top: 0px;
        left: 0;
        top: 0;
        justify-content: space-around;
        width: 100%;
        height: 100%;
        overflow: auto;
        background-color: rgb(0,0,0);
        background-color: rgba(0,0,0,0.9);
    }

    .image-modal-content {
        display: flex;
        justify-content: space-around;
        alignment-baseline: central;
        width: 100%;
        height: auto;
        max-height:
    }

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

    .buttonCarousel {
        position: absolute;
        color: #999 !important;
        font-size: 31px;
        transition: 0.3s;
    }

    #closeImageButton {
        position: absolute;
        top: 10px;
        right: 20px;
    }

    #deleteImageButton,
    #downloadImageButton {
        color: #AAA !important;
        font-size: 15px;
        margin: 5px;
    }

    #deleteImageButton:hover,
    #deleteImageButton:focus,
    #downloadImageButton:hover,
    #downloadImageButton:focus {
        color: #FFF !important;
        cursor: pointer;
    }

    .bottomButtons {
        position: absolute;
        transition: 0.3s;
        bottom: 5px;
        width: auto;
    }

    .buttonCarousel:hover,
    .buttonCarousel:focus {
        color: #FFF !important;
        text-decoration: none;
        cursor: pointer;
    }

    .carouselButton {
        display: flex;
        flex-direction: column;
        justify-content: space-around;
        overflow: visible;
        text-align: center;
        width: 100% !important;
        font: 40px;
        color: #CCC !important;
        background-color: rgba(0, 0, 0, 0) !important;
        height: 100% !important;
        font-weight: bold;
        transition: 0.3s;
    }

    .carouselButton:hover,
    .carouselButton:focus {
        color: #FFF !important;
        text-decoration: none;
        cursor: pointer;
    }

    #prevButton span {
        position: absolute;
        left: 10px;
    }

    #nextButton span {
        position: absolute;
        right: 10px;
    }

    .innerContent {
        width: 100%;
        height: 100%;
        display: flex;
        text-align: center;
    }

    #overIBS {
        display: flex;
        flex-direction: column;
        justify-content: space-around;
        width: auto;
        height: 100%;
        max-height: 100vh;
    }
</style>
