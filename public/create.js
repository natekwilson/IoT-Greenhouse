var app = new Vue({
  el: '#admin',
  data: {
    title: "",
    file: null,
    addItem: null,
    items: [],
    findTitle: "",
    findItem: null,
  },
  methods: {
  fileChanged(event) {
      this.file = event.target.files[0]
    },
    async upload() {
      try {
        const formData = new FormData();
        formData.append('photo', this.file, this.file.name)
        let r1 = await axios.post('/api/photos', formData);
        let r2 = await axios.post('/api/items', {
          title: this.title,
          path: r1.data.path,
          score: 0
        });
        this.addItem = r2.data;
      } catch (error) {
        console.log(error);
      }
    },
    async summon() {
      console.log("In Fetch ");
      var url = "https://api.thecatapi.com/v1/images/search";
      console.log("URL " + url);
      fetch(url)
        .then((data) => {
          return (data.json());
        })
        .then((output) => {
          console.log("upload");
          this.file= output.url;
        });
    },
  async getItems() {
  	try {
    	let response = await axios.get("/api/items");
    	this.items = response.data;
   	 return true;
  	} catch (error) {
   	console.log(error);
  	}
    },
   selectItem(item) {
      this.findTitle = "";
      this.findItem = item;
    },
    async changeItem(item) {
      try {
        let response = await axios.put("/api/change/" + item._id, {
          title: this.findItem.title,
        });
        this.findItem = null;
        this.getItems();
        return true;
      } catch (error) {
        console.log(error);
      }
    }, 
  },
  created() {
    this.getItems();
  },
  computed: {
    suggestions() {
      return this.items.filter(item => item.title.toLowerCase().startsWith(this.findTitle.toLowerCase()));
    },
    sortedArray: function() {
      function compare(a, b) {
        if (a.score < b.score)
          return -1;
        if (a.score > b.score)
          return 1;
        return 0;
      }
        return this.items.sort(compare);
    }
  },
});
