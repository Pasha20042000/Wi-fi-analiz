///
/// \file Util/RingDeque.hpp
///
/// A templated double ended queue implemented on top of a vector.
///
/// \copyright
/// Copyright (c) 2013-2017 Josh Blum
/// SPDX-License-Identifier: BSL-1.0
///

#pragma once
#include <Pothos/Config.hpp>
#include <cstdlib> //size_t
#include <utility> //forward
#include <memory> //allocator
#include <cassert>

namespace Pothos {
namespace Util {

/*!
 * RingDeque is a templated deque using an underlying vector.
 * The API of RingDeque is very similar to the std::deque<T>.
 * RingDeque is here because I wanted the efficiency of
 * boost::circular_buffer without the boost requirement.
 * The ring deque does not have a specific capacity limit.
 */
template <typename T, typename Allocator = std::allocator<T>>
class RingDeque
{
public:
    /*!
     * Construct a new ring deque
     * \param capacity the maximum space available
     * \param allocator an optional custom allocator
     */
    RingDeque(const size_t capacity = 1, const Allocator &allocator = Allocator());

    //! Copy constructor
    RingDeque(const RingDeque<T, Allocator> &other);

    //! Move constructor
    RingDeque(RingDeque<T, Allocator> &&other);

    //! Copy assignment
    RingDeque &operator=(const RingDeque<T, Allocator> &other);

    //! Move assignment
    RingDeque &operator=(RingDeque<T, Allocator> &&other);

    //! Destruct the ring queue and any elements held
    ~RingDeque(void);

    //! Get a const ref at, where front == 0, back == size() - 1
    const T &operator[](const size_t offset) const;

    //! Get a ref at, where front == 0, back == size() - 1
    T &operator[](const size_t offset);

    //! Push an element onto the front of the queue
    template <typename U>
    void push_front(U &&elem);

    //! Emplace an element onto the front of the queue
    template <typename... Args>
    T &emplace_front(Args&&... args);

    //! Pop and element from the front of the queue
    void pop_front(void);

    //! Get a const reference to the front element
    const T &front(void) const;

    //! Get a reference to the front element
    T &front(void);

    //! Push an element onto the back of the queue
    template <typename U>
    void push_back(U &&elem);

    //! Emplace an element onto the back of the queue
    template <typename... Args>
    T &emplace_back(Args&&... args);

    //! Pop and element from the back of the queue
    void pop_back(void);

    //! Get a const reference to the back element
    const T &back(void) const;

    //! Get a reference to the back element
    T &back(void);

    //! Is the deque empty? -- no elements
    bool empty(void) const;

    //! Is the deque full? -- num elements == capacity
    bool full(void) const;

    //! How many elements are in the deque
    size_t size(void) const;

    //! How many elements can be stored?
    size_t capacity(void) const;

    //! Set the deque capacity if too small
    void set_capacity(const size_t capacity);

    //! Empty the contents of this queue
    void clear(void);

    typedef T value_type; //!< The element type

    typedef Allocator allocator_type; //!< The allocator type

private:
    Allocator _allocator;
    size_t _mask;
    size_t _capacity;
    size_t _frontIndex;
    size_t _numElements;
    T *_container;
};

namespace Detail {

    template <typename T>
    T nextPow2(const T &in)
    {
        T out(1);
        while (out < in) out <<= 1;
        return out;
    }

} //namespace Detail

template <typename T, typename A>
RingDeque<T, A>::RingDeque(const size_t capacity, const A &allocator):
    _allocator(allocator),
    _mask(Detail::nextPow2(capacity)-1),
    _capacity(capacity),
    _frontIndex(0),
    _numElements(0),
    _container(_allocator.allocate(_mask+1))
{
    assert(capacity > 0);
}

template <typename T, typename A>
RingDeque<T, A>::RingDeque(const RingDeque<T, A> &other):
    _mask(other._mask),
    _capacity(other._capacity),
    _frontIndex(0),
    _numElements(0),
    _container(_allocator.allocate(_mask+1))
{
    for (size_t i = 0; i < other.size(); i++)
    {
        this->push_back(other[i]);
    }
}

template <typename T, typename A>
RingDeque<T, A>::RingDeque(RingDeque<T, A> &&other):
    _allocator(std::move(other._allocator)),
    _mask(std::move(other._mask)),
    _capacity(std::move(other._capacity)),
    _frontIndex(std::move(other._frontIndex)),
    _numElements(std::move(other._numElements)),
    _container(std::move(other._container))
{
    other._numElements = 0;
    other._capacity = 0;
    other._container = nullptr;
}

template <typename T, typename A>
RingDeque<T, A> &RingDeque<T, A>::operator=(const RingDeque<T, A> &other)
{
    this->clear();
    this->set_capacity(other.capacity());
    for (size_t i = 0; i < other.size(); i++)
    {
        this->push_back(other[i]);
    }
    return *this;
}

template <typename T, typename A>
RingDeque<T, A> &RingDeque<T, A>::operator=(RingDeque<T, A> &&other)
{
    this->clear();
    _allocator.deallocate(_container, _mask+1);
    _allocator = std::move(other._allocator);
    _mask = std::move(other._mask);
    _capacity = std::move(other._capacity);
    _frontIndex = std::move(other._frontIndex);
    _numElements = std::move(other._numElements);
    _container = std::move(other._container);
    other._numElements = 0;
    other._capacity = 0;
    other._container = nullptr;
    return *this;
}

template <typename T, typename A>
RingDeque<T, A>::~RingDeque(void)
{
    if (_container == nullptr) return;
    this->clear();
    _allocator.deallocate(_container, _mask+1);
}

template <typename T, typename A>
const T &RingDeque<T, A>::operator[](const size_t offset) const
{
    return _container[(_frontIndex + offset) & _mask];
}

template <typename T, typename A>
T &RingDeque<T, A>::operator[](const size_t offset)
{
    return _container[(_frontIndex + offset) & _mask];
}

template <typename T, typename A>
template <typename U>
void RingDeque<T, A>::push_front(U &&elem)
{
    this->emplace_front(std::forward<U>(elem));
}

template <typename T, typename A>
template <typename... Args>
T &RingDeque<T, A>::emplace_front(Args&&... args)
{
    assert(not this->full());
    _frontIndex--;
    _numElements++;
    return *(new(&front()) T(std::forward<Args>(args)...));
}

template <typename T, typename A>
void RingDeque<T, A>::pop_front(void)
{
    assert(not this->empty());
    this->front().~T();
    _frontIndex++;
    _numElements--;
}

template <typename T, typename A>
const T &RingDeque<T, A>::front(void) const
{
    assert(not this->empty());
    return (*this)[0];
}

template <typename T, typename A>
T &RingDeque<T, A>::front(void)
{
    assert(not this->empty());
    return (*this)[0];
}

template <typename T, typename A>
template <typename U>
void RingDeque<T, A>::push_back(U &&elem)
{
    this->emplace_back(std::forward<U>(elem));
}

template <typename T, typename A>
template <typename... Args>
T &RingDeque<T, A>::emplace_back(Args&&... args)
{
    assert(not this->full());
    _numElements++;
    return *(new(&back()) T(std::forward<Args>(args)...));
}

template <typename T, typename A>
void RingDeque<T, A>::pop_back(void)
{
    assert(not this->empty());
    this->back().~T();
    _numElements--;
}

template <typename T, typename A>
const T &RingDeque<T, A>::back(void) const
{
    assert(not this->empty());
    return (*this)[size_t(_numElements-1)];
}

template <typename T, typename A>
T &RingDeque<T, A>::back(void)
{
    assert(not this->empty());
    return (*this)[size_t(_numElements-1)];
}

template <typename T, typename A>
bool RingDeque<T, A>::empty(void) const
{
    return _numElements == 0;
}

template <typename T, typename A>
bool RingDeque<T, A>::full(void) const
{
    return _numElements == _capacity;
}

template <typename T, typename A>
size_t RingDeque<T, A>::size(void) const
{
    return _numElements;
}

template <typename T, typename A>
size_t RingDeque<T, A>::capacity(void) const
{
    return _capacity;
}

template <typename T, typename A>
void RingDeque<T, A>::set_capacity(const size_t capacity)
{
    if (_numElements > capacity) return;
    RingDeque<T, A> newRing(capacity);
    while (not this->empty())
    {
        newRing.push_back(std::move(this->front()));
        this->pop_front();
    }
    *this = std::move(newRing);
}

template <typename T, typename A>
void RingDeque<T, A>::clear(void)
{
    while (not this->empty())
    {
        this->pop_front();
    }
}

} //namespace Util
} //namespace Pothos
