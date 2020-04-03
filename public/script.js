var app = new Vue({
  el: '#app',
  data: {
  items: [],
  },
  methods: {
  async getItems(item) {
      try {
        let response = await axios.get("/api/items");
        this.items = response.data;
        return true;
      } catch (error) {
        console.log(error);
      }
    },
    async upItem(item) {
      console.log("changing ", item.title)
        try {
          let response = await axios.put("/api/items/" + item._id, {
            score: (item.score + 1),
          });
          this.getItems();
        } catch (error) {
          console.log(error);
        }
    },
    async downItem(item) {
      console.log("changing ", item.title)
        try {
          let response = await axios.put("/api/items/" + item._id, {
            score: (item.score - 1),
          });
          this.getItems();
        } catch (error) {
          console.log(error);
        }
    },
  },
  created() {
    this.getItems();
  },
  computed: {
    sortedArray: function() {
      function compare(a, b) {
        if (a.score > b.score)
          return -1;
        if (a.score < b.score)
          return 1;
        return 0;
      }
        return this.items.sort(compare);
    }
  }
});
