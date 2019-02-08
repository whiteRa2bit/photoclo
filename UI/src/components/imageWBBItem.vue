<template>
    <div id="id1">
    	<div class="myContainer">
        	<img id="image-WBB-Item" v-bind:src="image.url" alt="" />
            <bbButton class="btn" v-for="(face, index) in faces" v-bind:style="getStyle(index)"/>
        </div>
    </div>
</template>

<script>
    import bbButton from './bbButton.vue';

	export default {
		name: 'imageWBBItem',
        components: {
            bbButton
        },
		props: {
            image: {
                type: Object,
                default () {
                    return {};
                }
            },
            faces: {
                type: Object,
                default() {
                    return {};
                }
            }
        },
        methods: {
            getStyle(index) {
                console.log('Voop-Voop-Voop');
                var x1 = this.faces[index].bounding_box[0];
                var y1 = this.faces[index].bounding_box[1];
                var x2 = this.faces[index].bounding_box[2];
                var y2 = this.faces[index].bounding_box[3];
                var height = y2 - y1;
                var width = x2 - x1;
                var st = '';
                console.log(x1, y1, x2, y2, this.image.height, this.image.width);
                st = st + 'height: ' + String(height * 100 / this.image.height) + '%;';
                st = st + 'width: ' + String(width * 100 / this.image.width) + '%;';
                st = st + 'left: ' + String((x1 + x2) * 50 / this.image.width) + '%;';
                st = st + 'top: ' + String((y1 + y2) * 50 / this.image.height) + '%;';
                console.log('its a sound of the police');
                console.log(st);
                return st;
            }
        }
	}
</script>

<style scoped>
    #image-WBB-Item {
        image-orientation: from-image;
    }

    #id1 {
        display: flex;
        flex-direction: column;
        justify-content: space-around;
        width: 100%;
        height: 100%;
    }

    .myContainer {
        position: relative;
        width: 100%;
        height: auto;
    }

    /* Make the image responsive */
    .myContainer img {
        width: 100%;
        max-width: 100%;
        max-height: 100%;
    }

    /* Style the button and place it in the middle of the container/image */
    .myContainer .btn {
        position: absolute;
        transform: translate(-50%, -50%);
        -ms-transform: translate(-50%, -50%);
        border: none;
        cursor: pointer;
        border-radius: 5px;
    }
</style>