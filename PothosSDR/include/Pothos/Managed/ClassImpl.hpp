///
/// \file Managed/ClassImpl.hpp
///
/// Template implementation details for ManagedClass.
///
/// \copyright
/// Copyright (c) 2013-2016 Josh Blum
/// SPDX-License-Identifier: BSL-1.0
///

#pragma once
#include <Pothos/Config.hpp>
#include <Pothos/Callable/CallableImpl.hpp>
#include <Pothos/Managed/Class.hpp>
#include <functional> //std::reference_wrapper

namespace Pothos {

namespace Detail {

template <typename T>
std::reference_wrapper<T> referenceToWrapper(T &v)
{
    return std::ref(v);
}

template <typename T>
std::reference_wrapper<T> pointerToWrapper(T *v)
{
    return std::ref(*v);
}

template <typename T>
std::reference_wrapper<T> sharedToWrapper(std::shared_ptr<T> &v)
{
    return std::ref(*v);
}

template <typename T, typename Base>
std::reference_wrapper<Base> convertToBase(T &v)
{
    return std::ref<Base>(v);
}

template <typename T>
void deleteValue(T &v)
{
    delete (&v);
}

template <typename ClassType, typename ValueType>
static const ValueType &getField(ClassType &i, const std::function<ValueType &(ClassType *)> &getRef)
{
    return getRef(&i);
}

template <typename ClassType, typename ValueType>
static void setField(ClassType &i, const std::function<ValueType &(ClassType *)> &getRef, const ValueType &v)
{
    getRef(&i) = v;
}

} //namespace Detail

template <typename ClassType>
ManagedClass &ManagedClass::registerClass(void)
{
    if (not getReferenceToWrapper() or not getPointerToWrapper() or not getSharedToWrapper())
    {
        registerReferenceToWrapper(Callable(&Detail::referenceToWrapper<ClassType>));
        registerPointerToWrapper(Callable(&Detail::pointerToWrapper<ClassType>));
        registerSharedToWrapper(Callable(&Detail::sharedToWrapper<ClassType>));
        registerMethod("delete", Callable(&Detail::deleteValue<ClassType>));
    }
    return *this;
}

template <typename ClassType, typename BaseClassType>
ManagedClass &ManagedClass::registerBaseClass(void)
{
    return this->registerToBaseClass(Callable(&Detail::convertToBase<ClassType, BaseClassType>));
}

template <typename ClassType, typename ValueType>
ManagedClass &ManagedClass::registerField(const std::string &name, ValueType ClassType::*member)
{
    std::function<ValueType &(ClassType *)> getRef = std::mem_fn(member);
    this->registerMethod("get:"+name, Callable(&Detail::getField<ClassType, ValueType>).bind(getRef, 1));
    this->registerMethod("set:"+name, Callable(&Detail::setField<ClassType, ValueType>).bind(getRef, 1));
    return *this;
}

template <typename ClassType, typename... ArgsType>
ManagedClass &ManagedClass::registerConstructor(void)
{
    this->registerClass<ClassType>();
    this->registerConstructor(Callable::factory<ClassType, ArgsType...>());
    this->registerStaticMethod("new", Callable::factoryNew<ClassType, ArgsType...>());
    this->registerStaticMethod("shared", Callable::factoryShared<ClassType, ArgsType...>());
    return *this;
}

template <typename ReturnType, typename... ArgsType>
ManagedClass &ManagedClass::registerStaticMethod(const std::string &name, ReturnType(*method)(ArgsType...))
{
    this->registerStaticMethod(name, Callable(method));
    return *this;
}

template <typename ReturnType, typename ClassType, typename... ArgsType>
ManagedClass &ManagedClass::registerMethod(const std::string &name, ReturnType(ClassType::*method)(ArgsType...))
{
    this->registerClass<ClassType>();
    this->registerMethod(name, Callable(method));
    return *this;
}

template <typename ReturnType, typename ClassType, typename... ArgsType>
ManagedClass &ManagedClass::registerMethod(const std::string &name, ReturnType(ClassType::*method)(ArgsType...) const)
{
    this->registerClass<ClassType>();
    this->registerMethod(name, Callable(method));
    return *this;
}

template <typename ClassType>
ManagedClass &ManagedClass::registerOpaqueConstructor(void)
{
    this->registerClass<ClassType>();
    this->registerOpaqueConstructor(Callable::factory<ClassType, const Object *, const size_t>());
    return *this;
}

} //namespace Pothos
