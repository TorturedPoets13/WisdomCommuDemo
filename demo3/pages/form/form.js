// pages/form/form.js
const api = require("../../config/api.js")

Page({

  /**
   * 页面的初始数据
   */
  data: {
    avatar: "/images/camera.png",
    objectArray: [{
        id: 1,
        name: '#19'
      },
      {
        id: 2,
        name: '#20'
      },
      {
        id: 3,
        name: '#21'
      },
      {
        id: 4,
        name: '#22'
      }
    ],
    index: -1,
    name:""
  },

  postUser(e){

    wx.showLoading({
      title: '提交中',
      mask:true
    })

    wx.uploadFile({
      url: api.bank,
      filePath: this.data.avatar,
      name: 'avatar',
      formData: {
        'name': this.data.name,
        'area': this.data.objectArray[this.data.index].id
      },
      success(res) {
        console.log(res);
        // 上一个页面新增数据
        var dataDict = JSON.parse(res.data)
        var row = {
          id: dataDict.id,
          area: dataDict.area_text,
          name: dataDict.name,
          avatar: dataDict.avatar,
        }
        var pages = getCurrentPages();
        var prevPage = pages[pages.length - 2]; //上一个页面
        prevPage.addRow(row)

        
        wx.navigateBack({})


        
        // 跳转会上一页
        wx.navigateBack({});
     
      },
      complete() {
        wx.hideLoading()
      }
    })


  },
  bindPickerChange(e) {
    this.setData({
      index: e.detail.value
    })
  },
  bindNameChange(e){},
  bindToCamera(e){
    wx.navigateTo({
      url: '/pages/camera/camera',
    })
  },
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(options) {

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

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom() {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage() {

  }
})