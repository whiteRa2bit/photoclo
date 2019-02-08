<template>
	<button class="mybbButton" />
</template>

<script>

	export default {
		name: 'bbButton',
		props: ['srcWidth', 'srcHeight', 'face', 'ids'],
        watch: {},
		methods: {},
        updated: function () {
                console.log('Voop-Voop-Voop');
                var bt = document.getElementsByClassName('mebbButton')[this.ids];
                var x1 = this.face.bounding_box[0];
                var y1 = this.face.bounding_box[1];
                var x2 = this.face.bounding_box[2];
                var y2 = this.face.bounding_box[3];
                var height = y2 - y1;
                var width = x2 - x1;
                bt.style.height = String(height * 100 / this.srcHeight) + '%';
                bt.style.width = String(width * 100 / this.srcWidth) + '%';
                bt.style.paddingLeft = String(x1 * 100 / this.srcWidth) + '%';
                bt.style.paddingTop = String(y1 * 100 / this.srcHeight) + '%';
                console('its a sound of the police');
        }
	}
</script>

<style scoped>
    .mybbButton {
        background-color: rgba(0, 0, 0, 0) !important;
        border: 2px yellow !important;
        position: absolute;
        margin: 0px !important;
    }
</style>