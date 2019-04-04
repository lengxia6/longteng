import axios from 'axios';

let base = '/api';

export const requestLogin = params => { return axios.post(`${base}/login`, params).then(res => res.data); };

export const getProjectListPage = params => { return axios.get(`${base}/project/list`, { params: params }); };

export const removeProject = params => { return axios.post(`${base}/project/delete`, params); };

export const batchRemoveProject = params => { return axios.post(`${base}/project/batchdelete`, params); };

export const editProject = params => { return axios.post(`${base}/project/edit`, params); };

export const addProject = params => { return axios.post(`${base}/project/add`,  params); };