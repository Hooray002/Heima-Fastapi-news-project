import { defineStore } from 'pinia'
import axios from 'axios'
import { apiConfig } from '../../config/api'

const DEFAULT_PAGE_SIZE = 10
const MORE_CATEGORY = { id: 10, name: '更多' }
const FALLBACK_CATEGORIES = [
  { id: 1, name: '头条' },
  { id: 2, name: '社会' },
  { id: 3, name: '国内' },
  { id: 4, name: '国际' },
  { id: 5, name: '娱乐' },
  { id: 6, name: '体育' },
  { id: 7, name: '科技' },
]

const isSuccessCode = (code) => code === 200 || code === '200'

const normalizeNewsItem = (item) => ({
  ...item,
  categoryId: item.categoryId ?? item.category_id,
  publishTime: item.publishTime ?? item.publish_time,
  relatedNews: Array.isArray(item.relatedNews) ? item.relatedNews.map(normalizeNewsItem) : []
})

export const useNewsStore = defineStore('news', {
  state: () => ({
    newsList: [],
    newsDetail: {},
    categories: [],
    currentCategory: 1,
    loading: false,
    refreshing: false,
    finished: false,
    categoriesLoading: false,
    listRequestId: 0
  }),

  actions: {
    async getCategories() {
      if (this.categoriesLoading) return

      this.categoriesLoading = true;

      try {
        const response = await axios.get(`${apiConfig.baseURL}/api/news/catogories`)
        const serverCategories = Array.isArray(response.data)
          ? response.data
          : (isSuccessCode(response.data?.code) && Array.isArray(response.data?.data) ? response.data.data : [])
        if (serverCategories.length) {
          const hasMoreCategory = serverCategories.some((item) => item.id === MORE_CATEGORY.id)
          this.categories = hasMoreCategory
            ? serverCategories
            : [...serverCategories, MORE_CATEGORY]

          if (!this.currentCategory && this.categories.length > 0) {
            this.currentCategory = this.categories[0].id
          }
          return
        }
      } catch (error) {
        console.error('获取新闻分类失败:', error)
      } finally {
        if (!this.categories.length) {
          this.categories = [...FALLBACK_CATEGORIES, MORE_CATEGORY]
        }
        this.categoriesLoading = false
      }
    },

    changeCategory(categoryId) {
      if (this.currentCategory === categoryId) return
      this.currentCategory = categoryId
      this.newsList = []
      this.finished = false
      this.loading = false
      this.refreshing = false
      this.listRequestId += 1
      this.getNewsList()
    },

    async getNewsList(isRefresh = false) {
      if (this.loading || (isRefresh && this.refreshing)) return

      const requestId = this.listRequestId
      const categoryId = this.currentCategory
      const currentLength = this.newsList.length

      if (isRefresh) {
        this.refreshing = true
        this.newsList = []
        this.finished = false
      }

      this.loading = true

      try {
        const params = {
          catogoryId: categoryId,
          page: isRefresh ? 1 : Math.ceil(currentLength / DEFAULT_PAGE_SIZE) + 1,
          pageSize: DEFAULT_PAGE_SIZE
        }

        const response = await axios.get(`${apiConfig.baseURL}/api/news/list`, { params })
        if (requestId !== this.listRequestId || categoryId !== this.currentCategory) {
          return
        }

        if (response.data && isSuccessCode(response.data.code)) {
          const newsData = Array.isArray(response.data?.data?.list)
            ? response.data.data.list.map(normalizeNewsItem)
            : []
          this.newsList = isRefresh ? newsData : [...this.newsList, ...newsData]
          if (newsData.length < params.pageSize) {
            this.finished = true
          }
        }
      } catch (error) {
        console.error('获取新闻列表失败:', error)
      } finally {
        if (requestId === this.listRequestId && categoryId === this.currentCategory) {
          this.loading = false
          this.refreshing = false
        }
      }
    },

    async getNewsDetail(id) {
      this.newsDetail = {}

      try {
        const response = await axios.get(`${apiConfig.baseURL}/api/news/detail`, {
          params: { id }
        })

        if (response.data && isSuccessCode(response.data.code) && response.data.data) {
          this.newsDetail = normalizeNewsItem(response.data.data)
          return
        }
      } catch (error) {
        console.error('获取新闻详情失败:', error)
      }
    },

    getCategoryName(categoryId) {
      const category = this.categories.find(item => item.id === categoryId)
      return category ? category.name : '未知'
    }
  }
})