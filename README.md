# Privacy-Preserving COVID-19 Data Analysis Using Differential Privacy

This project focuses on building a user-friendly application that applies Differential Privacy (DP) techniques to analyze and predict COVID-19 patient risks using a large-scale dataset. By leveraging DP algorithms such as Gaussian Noise, Report Noisy Max, and the Exponential Mechanism, the project ensures patient confidentiality while delivering actionable insights.

---

## Table of Contents
- [Overview](#overview)
- [Motivation](#motivation)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
- [Contributors](#contributors)
- [Acknowledgments](#acknowledgments)
- [References](#references)
- [License](#license)

---

## Overview
This application enables privacy-preserving analysis of mortality rates and associated risk factors in COVID-19 patients through an interactive GUI. It uses Differential Privacy to ensure the security of sensitive health data while allowing healthcare professionals to perform critical analyses and predictions.

---

## Motivation
The COVID-19 pandemic emphasized the importance of secure data analysis in healthcare. This project addresses the critical need for privacy-preserving analytics by integrating Differential Privacy techniques. It ensures compliance with privacy regulations such as HIPAA and GDPR while providing insights that support public health decisions.

---

## Features
- **Privacy-preserving analysis**: Protects patient data by introducing controlled noise into query results.
- **Interactive GUI**: Allows users to analyze and visualize data securely through a user-friendly interface.
- **Custom Differential Privacy algorithms**: Implemented for both numerical and categorical queries using mechanisms such as Gaussian, Laplace, Report Noisy Max, and Exponential.

---

## Technologies Used
- **Programming Language**: Python
- **Libraries**:
  - [NumPy](https://numpy.org)
  - [Pandas](https://pandas.pydata.org)
  - [Matplotlib](https://matplotlib.org)
  - [ttkbootstrap](https://ttkbootstrap.readthedocs.io)
  - [IBM Diffprivlib](https://github.com/IBM/differential-privacy-library)
- **Dataset**: [COVID-19 Dataset](https://www.kaggle.com/datasets/meirnizri/covid19-dataset)

---

## Getting Started
### Prerequisites
Make sure you have Python 3.8 or higher installed on your system.

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/privacy-preserving-covid19-analysis.git
