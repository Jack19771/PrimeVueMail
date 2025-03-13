 <template>
    <div>
      <input type="text" v-model="currentUrl" @keyup.enter="updateUrl" placeholder="Enter URL" />
      <iframe :src="currentUrl" width="100%" height="500px" style="border: none;"></iframe>
    </div>
  </template>
  
  <script>
  export default {
    name: 'BrowserComponent',
    props: {
      url: {
        type: String,
        default: '',
      },
    },
    data() {
      return {
        currentUrl: this.url,
      };
    },
    methods: {
      updateUrl() {
        this.currentUrl = this.currentUrl;
      },
    },
  };
  </script>
  