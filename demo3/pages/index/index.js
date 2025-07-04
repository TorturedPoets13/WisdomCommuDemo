// pages/index/index.js

const api = require("../../config/api.js")

Page({
  /**
   * 页面的初始数据
   */
  data: {
    dataDict: {
      data: [
        {
        "id": 45,
        "name": "gaga",
        "area": "#19",
        "avatar": "http://0.0.0.0:8000/media/bank/2025/03/26/Da8MrcRbPrlP88ba2275f8eed46877cd88ee2fa37789.jpg"
      }
    ],
      today_count: 0,
      total_count: 0,
      lastId:10
    }
  },
  bindToStatistics(e){
    wx.navigateTo({
      url: '/pages/statistics/statistics'
    })
  },
  addRow(row){
    var dataList = this.data.dataDict.data  // [11,22,33]
    dataList.unshift(row) // js中的数组语法 .unshift往列表[11,22,33]前追加 .push则往后追加
    this.setData({
      ["dataDict.data"]:dataList,
      ["dataDict.total_count"]:this.data.dataDict.total_count + 1,
      ["dataDict.today_count"]:this.data.dataDict.today_count + 1
    })
  },
  bindToForm(e){
    wx.navigateTo({
      url: '/pages/form/form'
    })
  },
  refresh() {
    //1.发送网络请求
    //2.数据绑定
    wx.showLoading({
      mask: true
    })
    wx.request({
      url: api.bank,
      method: "GET",
      success: (res) => {
        this.setData({
          dataDict: res.data
        })
      },
      complete() {
        wx.hideLoading()
      }
    })

  },

  doDeleteRow(e){
    
    wx.showModal({
      title: '确认是否删除？',
      confirmColor: "#ff461f",
      success: (res) => {
        if (!res.confirm) {
          return
        }
        
        var nid = e.currentTarget.dataset.nid
        var index = e.currentTarget.dataset.index
        
        var dataList = this.data.dataDict.data
        dataList.splice(index,1)
        
        wx.showLoading({
          title: '删除中',
          mask:true
        })

        wx.request({
          url: api.bank + nid + '/',
          method:'DELETE',
          success:(res) =>{
            let total_count = this.data.dataDict.total_count - 1
            if(total_count <0){
              total_count = 0
            } 
        
            let today_count = this.data.dataDict.today_count - 1
            if(today_count <0){
              total_today_countcount = 0
            } 
            
            this.setData({
              ["dataDict.data"]:dataList,
              ["dataDict.total_count"]:total_count,
              ["dataDict.today_count"]:today_count
            })
          },
          complete() {
            wx.hideLoading()
          }
        })
       
      }
    })
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {
    //发送网络请求... 
    this.refresh();
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady() {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow() {

  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide() {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload() {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh() {
    this.refresh();
  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom() {
    console.log("到底了");
  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage() {

  }
})