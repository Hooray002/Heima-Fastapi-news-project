/**
 * API配置文件
 * 包含API基础URL和AI问答功能所需的API参数
 * 
 * BASEURL分为本地测试地址，和autodl测试地址
 */
const BASEURL_LOCAL = 'http://127.0.0.1:8000'
const BASEURL_AUTODL = 'https://u873181-nax9-5af8a2bd.westd.seetacloud.com:8443'
const BASEURL = import.meta.env.VITE_API_BASE_URL?.trim() || BASEURL_LOCAL

// API基础URL配置
export const apiConfig = {
  // 后端API基础URL
  baseURL: BASEURL, // 优先使用 VITE_API_BASE_URL，其次使用默认地址

}

export const aiChatConfig = {
  // 改为调用后端代理接口，避免在前端暴露真实密钥
  apiEndpoint: `${apiConfig.baseURL}/api/ai/chat`,
  sessionsEndpoint: `${apiConfig.baseURL}/api/ai/sessions`,
  sessionMessagesEndpoint: (sessionId) => `${apiConfig.baseURL}/api/ai/sessions/${sessionId}/messages`,

  // 使用的模型
  model: 'qwen3-max-preview'
}
