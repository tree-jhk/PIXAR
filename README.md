# PIXAR: Path-based Informative and eXplainAble Recommendation
### ***KIISE(한국정보과학회) KCC 2024 Summer Conference Accepted Paper (Poster)***
**This repository is an official implementation of the paper ["Path-based Explainable Recommender System Leveraging Knowledge Graphs and Large Language Models"](https://drive.google.com/file/d/1u1_L5rLM3M8_SEzIyhOwHdl8FfDgxk1g/view?usp=sharing).**

![PIXAR Framework](https://github.com/tree-jhk/boaz-airflow-llm-example/assets/97151660/2df4a206-311e-4f40-94eb-cee393be9074)

This study proposes the PIXAR (Path-based Informative and eXplainAble Recommendation) framework, which enhances the explainability of recommendation results by utilizing paths in knowledge graphs as inputs for LLMs.   
PIXAR is composed of three stages:   
**(1) Meaningful path exploration through Collaborative Beam Search  **
**(2) Information Compression  **
**(3) Explanation generation based on LLM  **
Experimental results show that PIXAR outperforms the existing LLM-based recommendation framework, LLMXRec, in terms of both performance and explainability by leveraging path information.   
Particularly, the Information Compression module enabled the LLM to better understand the path information and enhance recommendation explanations.  
This study empirically demonstrates the explainability of path-based methods proposed in previous research and suggests a new direction for recommendation systems utilizing knowledge graphs and LLMs.  

본 연구는 지식 그래프의 경로를 LLM의 입력으로 활용하여 추천 결과의 설명력을 높이는 PIXAR (Path-based Informative and eXplainAble Recommendation) 프레임워크를 제안한다. PIXAR는 세 단계로 구성되어 있다: (1) Collaborative Beam Search를 통한 유의미한 경로 탐색, (2) Information Compression을 통한 정보 압축, (3) LLM 기반 설명 생성. 실험 결과, PIXAR는 경로 정보를 활용해 기존 LLM 기반 추천 프레임워크인 LLMXRec보다 우수한 성능과 설명력을 보였다. 특히, Information Compression 모듈을 포함했을 때 LLM이 경로 정보를 더 잘 이해하고 추천 설명을 보강할 수 있었다. 본 연구는 기존 연구에서 제안된 경로 기반 설명 가능성을 실증적으로 입증하였으며, 지식 그래프와 LLM을 활용한 새로운 추천 시스템 연구 방향을 제시한다.
