# Modeling and Estimation of One-Shot Random Access for Finite-User Multichannel Slotted ALOHA Systems

**Chia-Hung Wei**, Ray-Guang Cheng, *Senior Member, IEEE*, and Shiao-Li Tsao

---

## Abstract
This paper presents a combinatorial model and approximation formulas to estimate the average number of successful and collided users for a one-shot random access in finite-user multichannel slotted ALOHA systems. The proposed model and approximation can be used to evaluate the performance of group paging for machine-type communication (MTC) in 3GPP LTE. Numerical results demonstrate the applicable range of the approximation formulas and the accuracy of the derived performance metrics.

**Index Terms**—Access success probability, collision probability, group paging, mean access delay.

---

## I. Introduction

**M**ULTICHANNEL slotted ALOHA systems have been widely used to model the random access channel of a cellular network. Several analytical models have been proposed to investigate the performance of the multichannel slotted ALOHA systems [1]–[3]. In these studies, the authors usually assumed that arrivals of new and backlogged users in each access cycle follow a Bernoulli distribution [1] or a Poisson distribution [2], [3] with a constant rate. Therefore, most of the studies focused on the steady-state behavior of the multichannel random access and adjusted system parameters to stabilize the channels [1], to reduce the mean access delay [2], or to maximize the throughput [3] based on a known Poisson or Bernoulli arrival rate and/or a constant successful transmission probability. Different to existing studies, this work aims to investigate the transient behavior of the random access channels accessed by a known number of machine-type communication (MTC) devices in a short observation interval.

Machine-type communication (MTC) or machine-to-machine communication (M2M) is a new service defined to facilitate machines communicating with each other over existing cellular networks [4]. Machine-type communication normally involves a large number of MTC devices to support a wide range of applications such as metering, road security, and consumer electronic devices. Concurrent accesses of mass devices to a radio network may result in intolerable delays, packet loss or even service unavailability for existing human-to-human (H2H) communication services. Group paging is a candidate solution proposed to throttle the MTC traffic intensity [4]. In group paging, a base station sends a paging message to activate a large number of devices to access the network simultaneously. The devices are not allowed to transmit messages to the network unless they are paged. The paged devices should follow a standard random access procedure to access the network and the failed devices should perform the random access procedure again to access the network until the retry limit is reached.

The group paging mechanism is similar to the group random-access (GRA) scheme [1] that reserves certain slots in each time period to a group of users to transmit their packets on a random-access basis. Both of them provide multiple random-access slots in an access cycle (or, time period in [1], time slot in [3], and random access slot in [3]). The group paging mechanism is similar to the fast retrial algorithm [2] in which each collided user randomly chooses an random access opportunity (RAO) [4] (or, channel slot in [1] or random access channel in [3]) and immediately re-transmits the random-access attempt in the next access cycle until a maximum number of retransmissions are reached. Different from the assumptions adopted in the existing studies, the number of devices in group paging is finite; new arrivals are generated only at the beginning of the first access cycle; and the number of contending devices in each access cycle is gradually decreased if any device successfully accesses the channel. In other words, the arrival rate and the successful transmission probability are considerably decayed in next access cycles. Due to the time-varying load, we cannot directly apply the existing analytical models to analyze the performance of MTC group paging.

To investigate the transient behavior of finite-user multi-channel slotted ALOHA systems, we need to know the number of successful users in one-shot random access performed in each access cycle. Hence, we propose a combinatorial model to derive the number of successful and collided users in one-shot random access. Fast approximation formulas, which can considerable reduce the computational complexity of the combinational model, are further presented to approximate the results derived from the analytical model. We use a simplified group paging as an example to show how the approximation formulas are used to estimate the number of successful users in each random access cycle and then derive the performance metrics within a target observation interval.

The rest of this work is structured as follows. The system model and the analytical model are described in Section II. Section III shows the numerical results. Conclusions are finally drawn in Section IV.

---

## II. System Model

This work considers a fixed number of $M$ devices performing random access in a multichannel slotted Aloha system. In this system, time is divided into fix-length 'access cycle.' Each access cycle contains $N$ RAOs. A simplified group paging, which sets the backoff indicator (BI) to zero as in the fast retrial algorithm [2], is considered. That is, all of the $M$ devices transmit their first random-access attempts at a randomly chosen RAO in the first access cycle when receiving the paging message. A device learns the success or failure of its random-access attempt immediately at the end of the access cycle. The collided devices immediately re-transmit their random-access attempts in the next access cycle. The processing delay of base station and the transmission time of the message part are ignored [1]–[3]. A total of $I_{max}$ access cycles are reserved and thus, the random access of a device is failed if its access is not successful during $I_{max}$ access cycles. Therefore, the behavior of finite-user multichannel random access in an observation interval containing $I_{max}$ access cycles is investigated.

### A. One-shot Random Access

Let $N_{i}$ be the number of RAOs reserved for the $i^{th}$ access cycle; and $N_{S, i}$ and $N_{C, i}$ be the average number of successful, and collided RAOs observed at the end of the $i^{th}$ access cycle. Consider the first access cycle that $M$ devices contend for $N_{1}$ RAOs. $N_{S, 1}$ and $N_{C, 1}$ can be determined using a combinatorial model. Let $p_{k}(M, N_{1})$ be the probability that $M$ devices send random access attempts in an access cycle and $k$ of the $N_{1}$ RAOs are collided. $p_{k}(M, N_{1})$ is equal to the probability that placing $M$ balls into $N_{1}$ bins and $k$ bins have at least two balls ($i_{j} \geq 2$, for $1 \leq j \leq k$) and the remaining bins have one or zero ball. $p_{k}(M, N_{1})$ is given by

$$
p_{k}(M,N_{1}) = \frac{C_{k}^{N_{1}}}{N_{1}^{M}} \sum_{i_{1}=2}^{M-2(k-1)} \dots \sum_{i_{k}=2}^{M-\sum_{j=1}^{k-1}i_{j}} C_{i_{1}}^{M} \dots C_{i_{k}}^{M-\sum_{j=1}^{k-1}i_{j}} C_{M-\sum_{j=1}^{k}i_{j}}^{N_{1}-k} \left(M-\sum_{j=1}^{k}i_{j}\right)!. \tag{1}
**$$

where $C_{k}^{n}$ is the number of $k$-combinations from a given set of $n$ elements ($C_{k}^{n}=0$, if $n < k$). $N_{C, 1}$ is the expected value of the bins that have at least two balls and can be derived as

$$
N_{C, 1} = \sum_{k=1}^{\min\{N_{1}, \lfloor \frac{M}{2} \rfloor \}} k p_{k}(M, N_{1}). \tag{2}
$$

$N_{S,1}$ is the expected values of the bins that have only one ball and is determined by

$$
\begin{aligned}
N_{S,1} = \sum_{k=0}^{\min\{N_1, \lfloor \frac{M}{2} \rfloor \}} \frac{C_k^{N_1}}{N_1^M} \sum_{i_1=2}^{M-2(k-1)} \dots \sum_{i_k=2}^{M-\sum_{j=1}^{k-1} i_j} C_{i_1}^M \dots \\
C_{i_k}^{M-\sum_{j=1}^{k-1} i_j} C_{M-\sum_{j=1}^{k} i_j}^{N_1-k} \left(M - \sum_{j=1}^{k} i_j\right)! \left(M - \sum_{j=1}^{k} i_j\right). \tag{3}
\end{aligned}
$$

Note that Eqs. (1)-(3) are derived based on the assumption that $M$ is an integer. However, the average number of contending devices, i.e. $N_{C,i}$, in each access cycle may not always an integer. A complete binomial analysis can be further derived based on the joint state probability of the number of devices that transmit their random-access attempts in each of the $I_{max}$ access cycle. However, the computational complexity of the approach is considerably high and may not be suitable for dynamic management of random access resources for MTC. Hence, we need to find approximation formulas to derive $N_{C, i}$ and $N_{S,i}$ for the second and future access cycles, i.e. $i \geq 2$.

The system that $M$ devices contending for $N_{1}$ RAOs in a random access slot with duration of one time unit is equivalent to a system has $N_{1}$ mini slots, where each mini slot contains one RAO and has duration of $1/ N_{1}$ time unit. A recent study in [3], [5] revealed that a slotted ALOHA system can be used to model the collision probability of the random access channel with Poisson arrival in LTE. Therefore, we use a slotted Aloha system with Poisson arrival rate $M$ devices in a time unit and slot duration $1/ N_{1}$ time unit to approximate the case that $M$ devices contend for $N_{1}$ RAOs in one-shot random access. The average number of success RAOs in one-shot random access observed in one time unit is equal to the successful probability of a mini slot multiply by $N_{1}$. The successful probability of a mini slot is the probability that only one device transmits in the time duration of $1/N_1$ (that is, $(M/N_1)e^{-(M/N_1)}$). Hence, Eq. (3) can be approximated by

$$
N_{S, 1} = M e^{-\frac{M}{N_{1}}}. \tag{4}
$$

The average number of collided RAOs of the one-shot random access observed in one time unit is equal to $N_{1}$ minus the sum of idle RAOs and success RAOs. The average number of idle RAOs is equal to $N_{1}$ multiple by the idle probability of a mini slot (that is, $N_{1} e^{-(M/N_1)}$). Thus, Eq. (2) can be approximated by

$$
N_{C,1} = N_{1} - M e^{-\frac{M}{N_{1}}} - N_{1} e^{-\frac{M}{N_{1}}}. \tag{5}
$$

It should be noted that the average number of successful devices in one-shot random access is equal to the average number of success RAOs. Therefore, we can use Eq. (4) to estimate the number of contending devices in each access cycle for a target observation interval, which helps us to investigate to transient behavior of the random access channels. In the following, we will demonstrate how to use the approximation formulas to derive the main performance metrics of access success probability, mean access delay, and collision probability [4] for the simplified group paging.

### B. Performance Metrics

Let $K_{i}$ be the average number of devices that transmit their random-access attempts in the $i^{th}$ access cycle. Initially, $K_{1} = M$. From Eq. (5), the average number of successful RAOs, $N_{S, i}$, can be approximated by

$$
N_{S,i} = K_{i} e^{-\frac{K_{i}}{N_{i}}}. \tag{6}
$$

The number of devices that transmit their random-access attempts in the $(i+1)^{th}$ access cycle is equal to the number of contending devices minus the number of successful devices in the $i^{th}$ access cycle. Hence, they can be iteratively predicted by

$$
K_{i+1} = K_{i} - N_{S,i} = K_{i}(1 - e^{-\frac{K_{i}}{N_{i}}}). \tag{7}
$$

The access success probability, $P_{S}$, which is defined as the probability to successfully complete the random access procedure within the maximum number of retransmissions [4], $I_{max}$, is estimated by

$$
P_{s} = \sum_{i=1}^{I_{max}} N_{S,i}/M. \tag{8}
$$

The mean access delay, $T_{a}$, which is defined as the delay for each random access procedure between the first random access attempt and the completion of the random access procedure for the successfully accessed devices [4], is estimated by

$$
T_{a} = \left( \sum_{i=1}^{I_{max}} i \times N_{S,i} \right) \Bigg/ \sum_{i=1}^{I_{max}} N_{S,i} \quad \text{(unit : access cycles)}. \tag{9}
$$

The collision probability, $P_{C}$, is defined as the ratio between the number of collided RAO and the overall number of RAO in the period of $I_{max}$ access cycles [4]. $P_{C}$ is estimated by

$$
P_{C} = \sum_{i=1}^{I_{max}} N_{C,i} \Bigg/ \sum_{i=1}^{I_{max}} N_{i}. \tag{10}
$$

---

## III. Numerical Results

Computer simulations were conducted to find the applicable range of parameters in using the approximation formulas and to verify the accuracy of the derived performance metrics for the simplified group paging. We implemented the simplified group paging in our simulation using C language. The parameters and the random access procedures confirm to the LTE standard specification [4]. An error-free wireless channel without capture effect was considered in the simulations [3]. In the simulations, each point represented the average value of $10^7$ samples. For each sample, the performance of system triggered by sending a single group paging message was collected. In the simulation, $N_{i}$ was set to be a constant ($N_{i} = N$ for $1 \leq i \leq I_{max}$).

The valid range of the approximation formulas in one-shot random access is shown in Figs. 1 and 2. Fig. 1 shows the outcomes of the analytical model (obtained from Eqs. (2) and (3)) and the outcomes of the approximation formulas (obtained from Eqs. (5) and (4)). The normalized values of success ($N_{S,1}/N$) and collided RAOs ($N_{C,1}/N$) for $N=3$ and 14 and integer valued of $M$ ranging from 1 to $10N$ were investigated. The simulation results were all coincided with the analytical results and thus, the simulation results are not shown on Fig. 1. It is found in Fig. 1 that the results derived from the approximation formulas are identical if $M/N$ is fixed. However, the analytical results further depend on $N$ even if $M/N$ is fixed. Fig. 2 demonstrates the approximation error of Fig. 1, which is the absolute difference of the analytical results and approximation results and normalized by the analytical results. It is found that the approximation error of $N_{S,1}/N$ may up to 200% for $N = 3$ and $M/N = 8$ and the approximation error can be reduced by increasing $N$. Therefore, the approximation formulas can only be used if $N$ is large.

Figures 3, 4, and 5 illustrated simulation results and the derived performance metrics of the access success probability, the mean access delay, and the collision probability of the simplified group paging obtained from Eq. (8) to (10) for $M = 100$, $N = 5$ to 45 and $I_{max} = 10$, respectively. The approximation error, which is the absolute difference of the approximation result and the simulation result and normalized by the analytical result, is also presented. The results show that the approximation error of the access success probability is high for small $N$ and the approximation error of the collision probability is small for all $N$, which are consistent with the results observed from Figs. 1 and 2. Different to Fig. 3, the approximation error of the mean access delay is quite small even if $N$ is small. It is because that the approximation error of $N_{S,i}$ in the numerator of Eq. (9) was neutralized by the error in the denominator. In the implementation, the network normally allocates a large $N$ to obtain a high access success probability, which ensures the applicability of the proposed approximation formulas.

---

## IV. Conclusions

This paper presented a combinatorial model and fast approximation formulas to analyze the average number of successful users for a one-shot random access in finite-user multichannel slotted ALOHA systems. Numerical results show that the approximation formulas are accurate if there are a large number of users (large $M$) contending the random access channel. We then use a simplified group paging, which is proposed to control the overload of MTC in 3GPP LTE, as an example to illustrate how the proposed approximation formulas are applied practically. Currently, we are trying to use the approximation formulas to analyze a general multi-channel slotted ALOHA system considering the effects such as power ramping, time-domain backoff, transmission error, etc. Another interesting research topic is to find a dynamic RAO allocation algorithm to adjust $N_{i}$ based on the estimated contending devices in each access cycle as did in [1] and [6].

---

## References

[1] I. Rubin, “Group random-access discipline for multi-access broadcast channels,” *IEEE Trans. Inf. Theory*, vol. 24, pp. 578–592, Sep. 1978.
[2] Y. J. Choi, S. Park, and S. Bahk, “Multichannel random access in OFDMA wireless network,” *IEEE J. Sel. Areas Commun.*, vol. 24, no. 3, pp. 603–613, Mar. 2006.
[3] P. Zhou, H. Hu, H. Wang, and H. H. Chen, “An efficient random access scheme for OFDMA systems with implicit message transmission,” *IEEE Trans. Wireless Commun.*, vol. 7, no. 7, July 2008.
[4] 3GPP TR 37.868, “RAN improvements for machine-type communications,” v. 1.0.0, Oct. 2010.
[5] R. G. Cheng, C. H. Wei, S. L. Tsao, and F. C. Ren, “RACH collision probability for machine-type communications,” *2012 IEEE VTC – Spring*.
[6] D. Baron and Y. Birk, “Multiple working points in multichannel ALOHA with deadlines,” *Wireless Networks*, vol. 8, no. 1, pp. 5–11, Jan. 2002.