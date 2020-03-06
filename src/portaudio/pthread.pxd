
from posix.time cimport timespec


ctypedef void pthread_start(void *) nogil


cdef extern from 'pthread.h' nogil:

    int PTHREAD_MUTEX_RECURSIVE

    ctypedef int pthread_t
    ctypedef int pthread_attr_t
    ctypedef int pthread_mutex_t
    ctypedef int pthread_mutexattr_t
    ctypedef int pthread_cond_t
    ctypedef int pthread_condattr_t

    int pthread_create(pthread_t* pthread, pthread_attr_t* attr, pthread_start*, void* arg)
    int pthread_cancel(pthread_t pthread)
    int pthread_join(pthread_t pthread, void** ret)

    int pthread_condattr_init(pthread_condattr_t* pthread_condattr)
    int pthread_condattr_destroy(pthread_condattr_t* pthread_condattr)

    int pthread_cond_init(pthread_cond_t* pthread_cond, pthread_condattr_t* pthread_condattr)
    int pthread_cond_destroy(pthread_cond_t* pthread_cond)
    int pthread_cond_wait(pthread_cond_t* pthread_cond, pthread_mutex_t* pthread_mutex)
    int pthread_cond_timedwait(pthread_cond_t* pthread_cond, pthread_mutex_t* pthread_mutex, timespec* abstime)
    int pthread_cond_signal(pthread_cond_t* pthread_cond)
    int pthread_cond_broadcast(pthread_cond_t* pthread_cond)

    int pthread_mutexattr_init(pthread_mutexattr_t* pthread_mutexattr)
    int pthread_mutexattr_destroy(pthread_mutexattr_t* pthread_mutexattr)
    int pthread_mutexattr_settype(pthread_mutexattr_t* pthread_mutexattr, int type_)

    int pthread_mutex_init(pthread_mutex_t* pthread_mutex, pthread_mutexattr_t* pthread_mutexattr)
    int pthread_mutex_destroy(pthread_mutex_t* pthread_mutex)
    int pthread_mutex_lock(pthread_mutex_t* pthread_mutex)
    int pthread_mutex_unlock(pthread_mutex_t* pthread_mutex)

