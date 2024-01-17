<template>
    <div>
        <h1>Autonomous Mobile Robot</h1>
        <div class="display">
            <div class='flex-container-button'>
                <button class='point-button' @click="displayCommand('map')">Show Map</button>
                <button class='point-button' @click="displayCommand('camera')">Show Camera</button>
            </div>
            <div class="flex-container-display">
                <div class="video-container" v-if="mapOpen === true">
                    <img :src="streamUrl" alt="map" />
                </div>
                <div class="video-container" v-if="cameraOpen === true">
                    <img :src="streamUrl" alt="camera" />
                </div>
            </div>
        </div>
        <div class="movement">
            <h3>Movement Control</h3>
            <input type="radio" id="automatic" value="Automatic" v-model="selectedOption">
            <label for="automatic">Automatic</label>
            <input type="radio" id="manual" value="Manual" v-model="selectedOption">
            <label for="manual">Manual</label>
            <div class="control">
                <AutomaticControl v-if="selectedOption === 'Automatic'" :ws="ws"/>
                <ManualControl v-else :ws="ws"/>
            </div>
            <h4 class="speed-info">Movement and speed information</h4> 
        </div>
    </div>
  </template>
  
<script>
    import AutomaticControl from './Automatic.vue'
    import ManualControl from './Manual.vue'
  
    export default {
        name: 'BaseTemplate',
        components: {
            AutomaticControl,
            ManualControl
        },
        data() {
            return {
                selectedOption: 'Automatic',
                mapOpen: false,
                cameraOpen: false,
                ws: new WebSocket('ws://192.168.29.219:8000')
            }
        },
        methods: {
            displayCommand(display) {
                if (display === 'camera') {
                    if (this.cameraOpen) {
                        this.cameraOpen = false
                    } else {
                        this.cameraOpen = true
                    }
                } else if (display === 'map') {
                    if (this.mapOpen) {
                        this.mapOpen = false
                    } else {
                        this.mapOpen = true
                    }
                }
            }
        }
    }
</script>

<style scoped>
    .movement {
        border: 1px solid #ddd;
        padding: 20px;
        margin: 10px 0;
        border-radius: 4px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        place-items: center;
    }

    .video-container {
        width: 320px; /* Adjust as needed */
        height: 150px; /* Adjust as needed */
        background-color: black;
    }
    .video-container img {
        width: 100%;
        height: 100%;
        object-fit: contain;
    }

    .display {
        border: 1px solid #ddd;
        padding: 5px;
        margin: 10px 0;
        border-radius: 4px;
        box-shadow: 0 2px 8px rgba(153, 104, 62, 0.486);
        place-items: center;
    }

    .speed-info {
        text-align: center;
        padding: 10px;
    }

    .flex-container-display {
        display: flex;
        justify-content: space-between;
        place-items: center;
        flex-direction: column;
        padding-top:20px;
    }
</style>